import argparse, json, pathlib, datetime, csv, sys

def _read_metrics(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    total = data.get("total") or data.get("n_total") or data.get("count") or 0
    passed = data.get("passed") or data.get("n_passed") or data.get("correct") or data.get("success") or 0
    failed = data.get("failed") or data.get("n_failed") or (total - passed if total else 0)
    acc = data.get("accuracy") or data.get("acc") or (passed/total if total else 0.0)
    return total, passed, failed, float(acc)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("metrics_path_or_dir")
    ap.add_argument("history_csv")
    args = ap.parse_args()

    p = pathlib.Path(args.metrics_path_or_dir)
    metrics_path = p if p.suffix == ".json" else p / "metrics.json"
    total, passed, failed, acc = _read_metrics(metrics_path)

    hist = pathlib.Path(args.history_csv)
    hist.parent.mkdir(parents=True, exist_ok=True)
    new_file = not hist.exists()
    with open(hist, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["timestamp","total","passed","failed","accuracy","metrics_path"])
        w.writerow([datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z",
                    total, passed, failed, round(acc,6), str(metrics_path)])
    print(f"Appended to {hist} | total={total} passed={passed} failed={failed} acc={round(acc,6)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
