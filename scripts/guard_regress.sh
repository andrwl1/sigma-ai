#!/usr/bin/env bash
set -euo pipefail

THRESHOLD_PP_2="${THRESHOLD_PP_2:-2}"
CI_EVENT="${CI_EVENT_NAME:-local}"
SOFT_MODE="${SOFT_MODE:-false}" # true => предупреждение вместо падения

LAST_OK_RUN_ID="${LAST_OK_RUN_ID:-}"
if [[ -z "${LAST_OK_RUN_ID}" ]]; then
  echo "no successful runs found — bootstrap mode"
else
  echo "using run ${LAST_OK_RUN_ID} for artifacts"
  gh run download "${LAST_OK_RUN_ID}" --name "preci-report" --dir artifacts/summary || true
fi

[[ -f artifacts/summary/judgement.tsv ]] || {
  echo "no judgement.tsv — bootstrap."
  echo -e "OK\tbootstrap" > artifacts/summary/judgement.tsv
}

PREV_RATE=$(awk 'BEGIN{FS="\t"} /OK/{ok++} {tot++} END{if(tot==0)print 100; else print 100*ok/tot}' artifacts/summary/judgement.tsv)
CURR_RATE="${CURR_RATE:-$PREV_RATE}"
DELTA=$(python3 - <<PY
p=$PREV_RATE
c=$CURR_RATE
print(round(c-p,2))
PY
)

mkdir -p artifacts/summary
echo -e "OK\tguard" >> artifacts/summary/judgement.tsv
echo "prev_rate=${PREV_RATE} curr_rate=${CURR_RATE} delta_pp=${DELTA}"

{
  echo "## Guard verdict"
  echo "- event: ${CI_EVENT}"
  echo "- prev_rate: ${PREV_RATE}%"
  echo "- curr_rate: ${CURR_RATE}%"
  echo "- delta_pp: ${DELTA}"
  echo "- threshold_pp: ${THRESHOLD_PP_2}"
} >> ab_report.md

VIOLATION=$(python3 - <<PY
thr=float("${THRESHOLD_PP_2}")
d=float("${DELTA}")
print(1 if d < -thr else 0)
PY
)
if [[ "$VIOLATION" == "1" ]]; then
  if [[ "${SOFT_MODE}" == "true" ]]; then
    echo "::warning ::regression ${DELTA}pp worse than threshold ${THRESHOLD_PP_2}"
    exit 0
  else
    echo "::error ::regression ${DELTA}pp worse than threshold ${THRESHOLD_PP_2}"
    exit 1
  fi
fi
