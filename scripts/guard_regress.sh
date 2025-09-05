#!/usr/bin/env bash
set -euo pipefail

# Папки
mkdir -p artifacts/local artifacts/cloud artifacts/summary

echo "== Prepare local =="
if [[ -f artifacts/summary/judgement.tsv ]]; then
  cp artifacts/summary/judgement.tsv artifacts/local/judgement.tsv
  [[ -f artifacts/summary/stability.tsv ]] && cp artifacts/summary/stability.tsv artifacts/local/stability.tsv || true
  echo "✓ local saved"
else
  echo "⚠️  artifacts/summary/judgement.tsv не найден — создаю пустую заглушку, чтобы не падать"
  printf "test\texpected\tgot\tverdict\n" > artifacts/local/judgement.tsv
fi

echo "== Fetch cloud artifact =="
# Скачиваем последний артефакт из GitHub Actions в artifacts/summary/*
./scripts/sync_artifacts.sh

echo "== Prepare cloud =="
cp artifacts/summary/judgement.tsv artifacts/cloud/judgement.tsv
[[ -f artifacts/summary/stability.tsv ]] && cp artifacts/summary/stability.tsv artifacts/cloud/stability.tsv || true
echo "✓ cloud saved"

echo "== Build A/B reports =="
python scripts/ab_report.py
python scripts/ab_diff.py

echo "== Check regressions =="
# Если есть отличия — падаем
if grep -qE 'Расхождений:\s+0$' artifacts/summary/ab_diff.md; then
  echo "✅ No regressions"
else
  echo "❌ Regressions found!"
  echo "----- ab_diff.md -----"
  cat artifacts/summary/ab_diff.md || true
  exit 1
fi
