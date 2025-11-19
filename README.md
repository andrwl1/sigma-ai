
# ∑AI Benchmarks

## Overview
Repository for automated benchmarking of LLMs with reproducible pipelines.

## Structure
- scripts/ – runners, guard, helpers
- tests/ – prompt corpora
- artifacts/ – results and plots
- .github/workflows/ – CI pipelines

## Quickstart
python -m venv .venv
source .venv/bin/activate
pip install -U pip matplotlib pandas

## Smoke test
LIMIT=30 MODE=smoke bash scripts/ab_benchmark.sh "llama3.1:8b" "llama3.1:8b"

## Nightly
LIMIT=500 MODE=nightly bash scripts/ab_benchmark.sh "llama3.1:8b" "llama3.1:8b"

## Outputs
- artifacts/summary/ab_diff.csv
- artifacts/plots/ab_plot.png
- artifacts/manifest.json

## Nightly usage
Run nightly: `gh workflow run nightly.yml --ref master`
Verify last run locally: `bash scripts/verify_t500.sh $(date +%F)`
Keep N runs: `bash scripts/retention.sh`

## T2000

Статус: **validated** (baseline зафиксирован, воспроизводимость подтверждена)

[![nightly_t2000](https://github.com/andrw1/sigma-ai/actions/workflows/nightly_t2000.yml/badge.svg)](../../actions/workflows/nightly_t2000.yml)
[![nightly_t2000_rollup](https://github.com/andrw1/sigma-ai/actions/workflows/nightly_t2000_rollup.yml/badge.svg)](../../actions/workflows/nightly_t2000_rollup.yml)

## Scientific Archive (T3000 Freeze)

The ΣAI Scientific Archive contains the cryptographically-validated and reproducible evidence bundles for the T3000 baseline.

All artifacts are immutable, publicly verifiable, and referenced in the `ARCHIVE_MANIFEST.md` with SHA256 commitments.
See: [ARCHIVE_MANIFEST.md](./ARCHIVE_MANIFEST.md)

### Included Bundles

| Artifact | Description |
|---------|-------------|
| **SIGMA_AI_T3000_PROOF.tar.gz** | Scientific proof bundle: logs, traces, freeze-snapshots, reproducibility outputs. |
| **SIGMA_T3000_COMPARISON.tar.gz** | Cloud-vs-local replication: unified A/B diff CSV, metrics reconciliation, stability validation. |
| **ΣAI_LEGAL_PROOF_SET1.tar.gz** | Notarized legal evidence set: affidavit, author claim, timestamps, SHA proofs. |

### Hash Verification

```bash
shasum -a 256 artifacts/releases/SIGMA_AI_T3000_PROOF.tar.gz
shasum -a 256 artifacts/releases/SIGMA_T3000_COMPARISON.tar.gz
shasum -a 256 artifacts/releases/ΣAI_LEGAL_PROOF_SET1.tar.gz
bash scripts/verify_t3000.sh $(date +%F)
```
