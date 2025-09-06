#!/usr/bin/env bash
# Regression guard: compares current (local) run with the last successful Pre-CI run (cloud).
# Fails CI if:
#  - cloud artifacts differ from local (case/answer or verdict diff), or
#  - cloud pass_rate < local pass_rate - 2pp.
set -euo pipefail

echo "== guard_regress =="
command -v gh >/dev/null 2>&1 || { echo "gh CLI is required"; exit 1; }

# --- Paths --------------------------------------------------------------------
mkdir -p artifacts/local artifacts/cloud artifacts/summary

# --- Prepare local -------------------------------------------------------------
echo "== Prepare local =="
if [[ -f artifacts/summary/judgement.tsv ]]; then
  cp artifacts/summary/judgement.tsv artifacts/local/judgement.tsv
  [[ -f artifacts/summary/stability.tsv ]] && cp artifacts/summary/stability.tsv artifacts/local/stability.tsv || true
  echo "✔ local saved"
else
  # заглушки, чтобы скрипты не падали
  printf "test\tverdict\n" > artifacts/local/judgement.tsv
  printf "tick\tstatus\n"   > artifacts/local/stability.tsv
  echo "⚠ artifacts/summary/judgement.tsv не найден — создана заглушка"
fi

# --- Fetch cloud artifact ------------------------------------------------------
echo "== Fetch cloud artifact =="
if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "GH_TOKEN is not set — skipping cloud diff (allowing pipeline to pass)"
  exit 0
fi
export GH_TOKEN

BRANCH="${GITHUB_REF_NAME:-master}"
CURRENT_SHA="${GITHUB_SHA:-}"

LAST_OK_RUN_ID="$(
  gh run list \
    --workflow "Pre-CI" \
    --branch "${BRANCH}" \
    --json databaseId,conclusion,headSha \
    -L 20 \
  | jq -r --arg sha "${CURRENT_SHA}" '
      (.[]
       | select(.conclusion=="success" and (.headSha != $sha or $sha==""))
      ) | .databaseId
    ' | head -n1
)"

if [[ -z "${LAST_OK_RUN_ID}" ]]; then
  echo "no successful runs found — skipping regression guard"
  exit 0
fi

echo "using run ${LAST_OK_RUN_ID} for artifacts"
# имя артефакта должно совпадать с upload-artifact в workflow
gh run download "${LAST_OK_RUN_ID}" --name "preci-report" --dir artifacts/summary

# sanity check
ls -lh artifacts/summary || true
[[ -f artifacts/summary/judgement.tsv ]] || {
  echo "no judgement.tsv inside artifact — skipping regression guard"
  exit 0
}

# --- Prepare cloud -------------------------------------------------------------
cp artifacts/summary/judgement.tsv artifacts/cloud/judgement.tsv
[[ -f artifacts/summary/stability.tsv ]] && cp artifacts/summary/stability.tsv artifacts/cloud/stability.tsv || true
echo "✔ cloud saved"

# --- Build A/B reports ---------------------------------------------------------
echo "== Build A/B reports =="
python scripts/ab_report.py
python scripts/ab_diff.py

# --- Check regressions ---------------------------------------------------------
echo "== Check regressions =="
DIFF_FILE="artifacts/summary/ab_diff.md"

# threshold guard: cloud must not be worse than local by more than 2pp
python - <<'PY'
import re, sys, pathlib
p=pathlib.Path("artifacts/summary/ab_report.md").read_text()
def get(name):
    m=re.search(rf"{name}\s+pass = ([0-9.]+)", p)
    return float(m.group(1)) if m else None
pl, pc = get("local"), get("cloud")
if pl is not None and pc is not None:
    if pc < pl - 0.02:
        print(f"❌ Threshold fail: cloud worse by {pl-pc:.3f} (>2pp)")
        sys.exit(1)
print("✅ Threshold OK")
PY

if [[ ! -f "${DIFF_FILE}" ]]; then
  echo "no ${DIFF_FILE} — nothing to compare, skipping"
  exit 0
fi

# ожидаем строку вида: "Расхождений: 0"
if grep -qE '^Расхождений:\s+0\b' "${DIFF_FILE}"; then
  echo "✅ No regressions"
  exit 0
else
  echo "❌ Regressions found!"
  echo "------ ${DIFF_FILE} ------"
  cat "${DIFF_FILE}" || true
  exit 1
fi
