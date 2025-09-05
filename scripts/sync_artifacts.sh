#!/usr/bin/env bash
set -euo pipefail

REPO="andrwl1/sigma-ai"
OUTDIR="artifacts/summary"
TMP="$(mktemp -d)"
mkdir -p "$OUTDIR"

for dep in gh jq unzip; do
  command -v "$dep" >/dev/null 2>&1 || { echo "missing: $dep"; exit 1; }
done

RUN_ID="$(gh run list -R "$REPO" -L 1 --json databaseId -q '.[0].databaseId')"
[ -n "$RUN_ID" ] || { echo "no runs"; exit 1; }

# список артефактов последнего рана
NAMES=$(gh api "repos/${REPO}/actions/runs/${RUN_ID}/artifacts" --jq '.artifacts[].name')

# выбрать подходящее имя
PICK=""
for p in artifacts summary pre-ci-report preci-report report ci-artifacts; do
  if echo "$NAMES" | grep -qx "$p"; then PICK="$p"; break; fi
done
[ -z "$PICK" ] && PICK="$(echo "$NAMES" | head -n1)"
[ -z "$PICK" ] && { echo "no artifacts in run ${RUN_ID}"; exit 1; }

echo "run: $RUN_ID"
echo "artifact: $PICK"

gh run download -R "$REPO" "$RUN_ID" --name "$PICK" --dir "$TMP"

# если прилетел zip — распакуем всё, иначе возьмём файлы как есть
SRC="$TMP"
if ls "$TMP"/*.zip >/dev/null 2>&1; then
  mkdir -p "$TMP/unz"
  for z in "$TMP"/*.zip; do unzip -oq "$z" -d "$TMP/unz"; done
  SRC="$TMP/unz"
fi

# разложить по именам
shopt -s nullglob
found_any=0
while IFS= read -r -d '' f; do
  base="$(basename "$f")"
  case "$base" in
    report.md|*report*.md)                      cp -f "$f" "$OUTDIR/report.md"; found_any=1 ;;
    judgement.tsv|judgment.tsv|*judge*.tsv)     cp -f "$f" "$OUTDIR/judgement.tsv"; found_any=1 ;;
    stability.tsv|*stability*.tsv)              cp -f "$f" "$OUTDIR/stability.tsv"; found_any=1 ;;
    *.tsv)                                      cp -f "$f" "$OUTDIR/$base"; found_any=1 ;;
    *.md) if [ ! -f "$OUTDIR/report.md" ]; then cp -f "$f" "$OUTDIR/report.md"; found_any=1; fi ;;
  esac
done < <(find "$SRC" -type f -maxdepth 2 -print0)

rm -rf "$TMP"
echo "saved to: $OUTDIR"
ls -la "$OUTDIR"
[ "$found_any" -eq 1 ] || { echo "note: no matching files found inside artifact $PICK"; exit 2; }
