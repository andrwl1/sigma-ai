import os, re, csv, pathlib, datetime
import matplotlib.pyplot as plt

ROOT = pathlib.Path(".")
OUT_DIR = ROOT / "artifacts" / "t1000"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CANDIDATES = [
    ROOT / "artifacts" / "t1000" / "latest" / "verify_summary.txt",
    ROOT / "verify_summary.txt",
    ROOT / "artifacts" / "summary" / "ab_report.md",
    ROOT / "artifacts" / "summary" / "ab_diff.csv",
]

def _parse_from_text(path: pathlib.Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    m_rows = re.search(r"rows\s*[:=]\s*(\d+)", text, re.I)
    m_pr = re.search(r"pass[_\s-]?rate\s*[:=]\s*([0-9.]+)", text, re.I)
    m_dp = re.search(r"delta[_\s-]?pp\s*[:=]\s*(-?[0-9.]+)", text, re.I)
    rows = int(m_rows.group(1)) if m_rows else None
    pr = float(m_pr.group(1)) if m_pr else None
    dp = float(m_dp.group(1)) if m_dp else None
    return rows, pr, dp

def _parse_from_ab_diff_csv(path: pathlib.Path):
    try:
        with path.open(newline="", encoding="utf-8", errors="ignore") as f:
            r = csv.reader(f)
            rows = sum(1 for _ in r) - 1
            return max(rows, 0), None, None
    except Exception:
        return None, None, None

def resolve_metrics():
    source = None
    rows = pr = dp = None
    for p in CANDIDATES:
        if not p.exists():
            continue
        source = p
        if p.suffix.lower() in {".txt", ".md"}:
            rows, pr, dp = _parse_from_text(p)
        elif p.suffix.lower() == ".csv":
            rows, pr, dp = _parse_from_ab_diff_csv(p)
        if any(v is not None for v in (rows, pr, dp)):
            break
    rows = int(rows) if rows is not None else 0
    pr = float(pr) if pr is not None else 0.0
    dp = float(dp) if dp is not None else 0.0
    return source, rows, pr, dp

def append_history(rows: int, pr: float, dp: float):
    hist = OUT_DIR / "metrics_history.csv"
    newfile = not hist.exists()
    ts = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    with hist.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if newfile:
            w.writerow(["timestamp", "suite", "rows", "pass_rate", "delta_pp"])
        w.writerow([ts, "t1000", rows, pr, dp])
    return hist

def plot_trend(hist_path: pathlib.Path):
    xs, ys = [], []
    with hist_path.open(encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            xs.append(row["timestamp"])
            try:
                ys.append(float(row["pass_rate"]))
            except:
                ys.append(0.0)
    if not xs:
        return None
    plt.figure(figsize=(6, 3))
    plt.plot(range(len(ys)), ys, marker="o")
    plt.xticks(range(len(xs)), xs, rotation=45, ha="right")
    plt.xlabel("time (UTC)")
    plt.ylabel("pass_rate")
    plt.title("T1000 pass_rate trend")
    plt.tight_layout()
    out_png = OUT_DIR / "passrate_local.png"
    plt.savefig(out_png)
    return out_png

def main():
    src, rows, pr, dp = resolve_metrics()
    hist = append_history(rows, pr, dp)
    png = plot_trend(hist)
    src_s = str(src.relative_to(ROOT)) if src else "n/a"
    print(f"rollup_ok source={src_s} rows={rows} pass_rate={pr} delta_pp={dp}")
    print(f"history: {hist}")
    if png:
        print(f"trend:   {png}")

if __name__ == "__main__":
    main()
