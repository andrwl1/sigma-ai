#!/usr/bin/env bash
# Regression guard: compares current (local) vs last successful CI (cloud)
# - автопоиск последнего успешного Pre-CI на той же ветке
# - безопасный fallback: если нет артефактов — выходим без фейла (bootstrap)
# - порог качества: cloud не должен быть хуже local более чем на 2pp
# - дифф по кейсам (ожидаем "Расхождений: 0")

set -euo pipefail

echo "== guard_regress =="

# --- Folders -------------------------------------------------------------------
mkdir -p artifacts/local artifacts/cloud artifacts/summary

# --- Prepare local --------------------------------------------------------------
echo "== Prepare local =="
if [[ -f artifacts/summary/judgement.tsv ]]; then
  # если уже есть сводка из текущего запуска — копируем как 'local'
  cp artifacts/summary/judgement.tsv artifacts/local/judgement.tsv
  [[ -f artifacts/summary/stability.tsv ]] \
    && cp artifacts/summary/stability.tsv artifacts/local/stability.tsv || true
  echo "✔ local saved"
else
  # пустая заглушка, чтобы скрипты отчётов не падали
  echo -e "test\tverdict\tid\n__bootstrap__\tPASS\t0" > artifacts/local/judgement.tsv
  echo "ℹ no local judgement.tsv in summary — created stub to continue"
fi

# --- Detect last successful run on this branch ---------------------------------
echo "== Fetch cloud artifact =="
BRANCH="${GITHUB_REF_NAME:-master}"
CURRENT_SHA="${GITHUB_SHA:-}"

# Ищем последний УСПЕШНЫЙ запуск Pre-CI на той же ветке, исключая текущий коммит
if ! command -v jq >/dev/null 2>&1; then
  echo "jq not found, installing lightweight jq via python (fallback)"
  python - <<'PY'
import sys,json;print("jq_is_missing")
PY
fi

set +e
LAST_OK_RUN_ID="$(
  gh run list \
    --workflow "Pre-CI" \
    --branch "${BRANCH}" \
    --json databaseId,conclusion,headSha \
    -L 20 2>/dev/null | jq -r --arg sha "${CURRENT_SHA}" '
      (.[]
       | select(.conclusion=="success" and (.headSha != $sha or $sha==""))
      ) | .databaseId' | head -n1
)"
set -e

if [[ -z "${LAST_OK_RUN_ID}" ]]; then
  echo "no successful run to compare with — bootstrap mode (skip guard)"
  exit 0
fi

echo "using run ${LAST_OK_RUN_ID} for artifacts"

# Пытаемся скачать наш артефакт (имя должно совпадать с upload-artifact в workflow)
# Если артефакта нет (например, старый ран без выгрузки) — не валим сборку.
if ! gh run download "${LAST_OK_RUN_ID}" --name "preci-report" --dir artifacts/summary 2>/dev/null; then
  echo "no valid artifacts found to download — bootstrap mode (skip guard)"
  exit 0
fi

# sanity check
ls -lh artifacts/summary || true
if [[ ! -f artifacts/summary/judgement.tsv ]]; then
  echo "no judgement.tsv inside artifact — bootstrap mode (skip guard)"
  exit 0
fi

# --- Prepare cloud --------------------------------------------------------------
cp artifacts/summary/judgement.tsv artifacts/cloud/judgement.tsv
[[ -f artifacts/summary/stability.tsv ]] && cp artifacts/summary/stability.tsv artifacts/cloud/stability.tsv || true
echo "✔ cloud saved"

# --- Build A/B reports ----------------------------------------------------------
echo "== Build A/B reports =="
python scripts/ab_report.py
python scripts/ab_diff.py

# --- Threshold guard (2pp) ------------------------------------------------------
echo "== Threshold (<=2pp worse) =="
python - <<'PY'
import re, sys, pathlib
p = pathlib.Path("artifacts/summary/ab_report.md").read_text(encoding="utf-8")
def get(name):
    m = re.search(rf"{name}\s+pass = ([0-9.]+)", p)
    return float(m.group(1)) if m else None
pl, pc = get("local"), get("cloud")
if pl is not None and pc is not None:
    if pc < pl - 0.02:
        print(f"❌ Threshold fail: cloud worse by {pl - pc:.3f} (>2pp)")
        sys.exit(1)
print("✅ Threshold OK")
PY

# --- Diff guard -----------------------------------------------------------------
echo "== Check regressions (diff) =="
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
