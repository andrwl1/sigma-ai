from pathlib import Path
import json

reports = Path("reports")
metrics_p = reports / "metrics.json"
plots_dir = reports / "plots"
plots = sorted(plots_dir.glob("*.png")) if plots_dir.exists() else []

metrics = {}
if metrics_p.exists():
    metrics = json.loads(metrics_p.read_text())

lines = ["# Daily Report", ""]
if metrics:
    lines += ["## Metrics", "```json", json.dumps(metrics, indent=2), "```", ""]
else:
    lines += ["## Metrics", "_no metrics_", ""]

if plots:
    lines += ["## Plots", f"Latest plot: {plots[-1].as_posix()}"]
else:
    lines += ["## Plots", "_no plots_"]

reports.mkdir(parents=True, exist_ok=True)
(reports / "README.md").write_text("\n".join(lines))
print("report: saved -> reports/README.md")
