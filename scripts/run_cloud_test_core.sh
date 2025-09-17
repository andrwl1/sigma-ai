#!/usr/bin/env bash
set -euo pipefail
: "${OPENAI_API_KEY:?OPENAI_API_KEY is required}"
: "${OPENAI_PROJECT:?OPENAI_PROJECT is required}"
ID="$1"
PROMPT="$2"
MODEL="${3:-gpt-4o-mini}"
mkdir -p artifacts/cloud
BODY="$(jq -n --arg m "$MODEL" --arg p "$PROMPT" '{model:$m, input:$p, temperature:0, max_output_tokens:64}')"
RESP="$(curl -sS https://api.openai.com/v1/responses -H "Authorization: Bearer ${OPENAI_API_KEY}" -H "OpenAI-Project: ${OPENAI_PROJECT}" -H "Content-Type: application/json" -d "$BODY")"
printf '%s' "$RESP" > "artifacts/cloud/${ID}.json"
jq -r '(.output_text // .output[0].content[0].text // .choices[0].message.content // "")' "artifacts/cloud/${ID}.json" | head -n 1 > "artifacts/cloud/${ID}.txt"
