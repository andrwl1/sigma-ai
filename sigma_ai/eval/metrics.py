import argparse, json, pathlib, datetime, csv, sys

def _read(p: pathlib.Path):
    with open(p, "r", encoding="utf-8") as f:
        d = json.load(f)
    total  = d.get("total")  or d.get("n_total") or d.get("count")   or 0
    passed = d.get("passed") or d.get("n_passed") or d.get("correct") or d.get("success") or 0
    failed = d.get("failed") or d.get("n_failed") or (total - passed if total else 0)
    acc    = d.get("accuracy") or d.get("acc") or (passed/total if total else 0.0)
    return total, passed, failed, float(acc)

def _dir_from_arg(s: str) -> pathlib.Path:
    p = pathlib.Path(s)
    if p.suffix:
        return p.parent
    return p

def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("metrics_path_or_dir", nargs="?")
    ap.add_argument("history_csv", nargs="?")
    ap.add_argument("--pred")
    ap.add_argument("--out")
    args, _ = ap.parse_known_args()

    history = args.history_csv or args.out
    if not history:
        print("metrics.py: need history csv via positional arg or --out", file=sys.stderr)
        return 2

    metrics_path = None
    if args.metrics_path_or_dir:
        mp = pathlib.Path(args.metrics_path_or_dir)
        if mp.suffix == ".json":
            metrics_path = mp
        else:
            metrics_path = _dir_from_arg(args.metrics_path_or_dir) / "metrics.json"
    elif args.pred:
        metrics_path = _dir_from_arg(args.pred) / "metrics.json"
    else:
        print("metrics.py: need metrics path/dir or --pred", file=sys.stderr)
        return 2

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
