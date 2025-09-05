#!/usr/bin/env bash
# Regression guard: compares current (local) run with the last successful Pre-CI run (cloud).
# Exits with non-zero code if any differences found.

set -euo pipefail

echo "== guard_regress =="
echo "runner: $(uname -a)"
command -v gh >/dev/null 2>&1 || { echo "gh CLI is required"; exit 1; }

# --- Paths --------------------------------------------------------------------
mkdir -p artifacts/local artifacts/cloud artifacts/summary

# --- Prepare local -------------------------------------------------------------
# If current run already produced a summary, reuse it; otherwise create a stub so scripts don't crash.
echo "== Prepare local =="
if [[ -f artifacts/summary/judgement.tsv ]]; then
  cp artifacts/summary/judgement.tsv artifacts/local/judgement.tsv
  [[ -f artifacts/summary/stability.tsv ]] && cp artifacts/summary/stability.tsv artifacts/local/stability.tsv || true
  echo "✔ local saved"
else
  # minimal header for pandas
  echo -e "test\tverdict\n" > artifacts/local/judgement.tsv
  echo -e "tick\tstatus\n"   > artifacts/local/stability.tsv
  echo "⚠ artifacts/summary/judgement.tsv не найден — создана заглушка"
fi

# --- Fetch cloud artifact ------------------------------------------------------
echo "== Fetch cloud artifact =="

# Require token only for download; if нет — мягко выходим (не ломаем весь job)
if [[ -z "${GH_TOKEN:-}" ]]; then
  echo "GH_TOKEN is not set — skipping cloud diff (allowing pipeline to pass)"
  exit 0
fi
export GH_TOKEN

# Find last successful Pre-CI run on this branch, excluding the current SHA (если доступен)
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

# Download only our artifact (what we publish in Pre-CI)
# Name must match the artifacts upload step in your workflow.
gh run download "${LAST_OK_RUN_ID}" --name "preci-report" --dir artifacts/summary

# Sanity check
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
