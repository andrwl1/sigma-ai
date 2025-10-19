from __future__ import annotations
import csv
import sys
from pathlib import Path
from collections import defaultdict
from statistics import mean
from datetime import datetime
import matplotlib.pyplot as plt

def pick_arg(paths, suffix: str) -> Path | None:
    for p in paths:
        if str(p).lower().endswith(suffix):
            return Path(p)
    return None

def parse_float(x: str) -> float | None:
    try:
        return float(x)
    except Exception:
        return None

def parse_date(x: str) -> datetime | None:
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d.%m.%Y", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(x, fmt)
        except Exception:
            continue
    return None

def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("-")]
    csv_path = pick_arg(args, ".csv")
    png_path = pick_arg(args, ".png")
    prefix = "t2000_"
    for a in args:
        if a.endswith("_") and any(a.startswith(f"t{x}000_") for x in ("1", "2", "3")):
            prefix = a
    if csv_path is None or png_path is None:
        print("Usage: trend.py <metrics_history.csv> <output.png> [suite_prefix]")
        return 2
    if not csv_path.exists():
        print(f"ERR: CSV not found: {csv_path}")
        return 2
    rows_by_date: dict[datetime, list[float]] = defaultdict(list)
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            print("ERR: CSV has no header")
            return 2
        for i, row in enumerate(reader, 1):
            label = (row.get("label") or row.get("suite") or row.get("name") or "").strip()
            if not label.startswith(prefix):
                continue
            value = None
            for k in ("value", "score", "metric_value"):
                if k in row:
                    value = parse_float(row[k])
                    if value is not None:
                        break
            if value is None:
                continue
            dt = None
            for k in ("date", "timestamp", "time"):
                if k in row and row[k].strip():
                    dt = parse_date(row[k].strip())
                    if dt is not None:
                        break
            if dt is None:
                dt = datetime.fromtimestamp(i)
            rows_by_date[dt].append(value)
    if not rows_by_date:
        print(f"WARN: no rows matched prefix '{prefix}' in {csv_path}")
        x, y = [], []
    else:
        x = sorted(rows_by_date.keys())
        y = [mean(rows_by_date[dx]) for dx in x]
    plt.figure(figsize=(8, 4.5))
    if x and y:
        plt.plot(x, y, marker="o")
    plt.title(f"{prefix.rstrip('_')} trend")
    plt.xlabel("date")
    plt.ylabel("value")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(png_path)
    plt.close()
    print(f"OK: saved plot to {png_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
