# Benchmarking Pipeline

## Modes
- Smoke (T30–T50)
- Nightly (T500)

## Steps
1. Run ab_benchmark.sh
2. Generate CSV and PNG
3. Write manifest.json
4. Guard checks
5. Pack artifacts
6. Retention (14)

## Guard
- Min rows
- Header check
- NaN filter
- Plot size

## Retention
- 14 runs kept
- Older runs packed into tar.zst
