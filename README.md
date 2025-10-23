
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
- Proof bundle: `artifacts/releases/SIGMA_AI_T3000_PROOF.tar.gz`
- Legal set: `artifacts/releases/ΣAI_LEGAL_PROOF_SET1.tar.gz`
- Baseline tag: `stable_t3000_sb1`

## Reproducible Release Protocol

The ∑AI framework adheres to a fully automated and verifiable release pipeline.

### Protocol Overview
Every release is cryptographically signed, validated, and published through a continuous integration workflow:
- Build artifacts generated via `python -m build`
- Metadata integrity verified with `twine check`
- SHA-256 checksums recorded and uploaded as part of the release manifest
- Dual-channel deployment:
  - Manual dispatch → TestPyPI
  - Tag push (`v*.*.*`) → PyPI

### Verification
All releases are reproducible and independently verifiable through the public CI/CD logs.

[![PyPI version](https://badge.fury.io/py/sigma-ai.svg)](https://pypi.org/project/sigma-ai/)
[![GitHub Actions](https://github.com/andrwl1/sigma-ai/actions/workflows/publish.yml/badge.svg)](https://github.com/andrwl1/sigma-ai/actions/workflows/publish.yml)

### Integrity Statement
Each build is a frozen scientific snapshot (“ΣAI Scientific Freeze”) and represents a reproducible state of the framework, ensuring traceability, transparency, and academic replicability.
