import argparse, json, pathlib, datetime, csv, sys

def _read(p):
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    total = d.get("total") or d.get("n_total") or d.get("count") or 0
    passed = d.get("passed") or d.get("n_passed") or d.get("correct") or d.get("success") or 0
    failed = d.get("failed") or d.get("n_failed") or (total - passed if total else 0)
    acc = d.get("accuracy") or d.get("acc") or (passed/total if total else 0.0)
    return total, passed, failed, float(acc)

def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("metrics_path_or_dir", nargs="?")
    p.add_argument("history_csv", nargs="?")
    p.add_argument("--pred")
    p.add_argument("--out")
    args, _ = p.parse_known_args()

    metrics_src = args.metrics_path_or_dir or args.pred
    history = args.history_csv or args.out
    if not metrics_src or not history:
        print("metrics.py: need metrics path/dir and history csv", file=sys.stderr)
        return 2

    mp = pathlib.Path(metrics_src)
    metrics_path = mp if mp.suffix == ".json" else (mp.parent / "metrics.json" if mp.is_file() else mp / "metrics.json")

    total, passed, failed, acc = _read(metrics_path)

    h = pathlib.Path(history)
    h.parent.mkdir(parents=True, exist_ok=True)
    new = not h.exists()
    with open(h, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp","total","passed","failed","accuracy","metrics_path"])
        w.writerow([datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z",
                    total, passed, failed, round(acc,6), str(metrics_path)])
    print(f"OK {h} total={total} passed={passed} failed={failed} acc={round(acc,6)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
