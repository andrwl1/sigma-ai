from pathlib import Path
import json
import pandas as pd

logs_dir = Path("logs")
logs = sorted(logs_dir.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
if not logs:
    print("metrics: no logs")
    raise SystemExit(0)

src = logs[0]
df = pd.read_csv(src)
stats = {}
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        s = df[col].dropna()
        if len(s):
            stats[col] = {
                "min": float(s.min()),
                "max": float(s.max()),
                "mean": float(s.mean()),
                "last": float(s.iloc[-1])
            }

out = Path("reports")
out.mkdir(parents=True, exist_ok=True)
(out / "metrics.json").write_text(json.dumps({"source": src.as_posix(), "stats": stats}, indent=2))
print("metrics: saved -> reports/metrics.json")
