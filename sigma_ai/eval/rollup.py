import argparse, pathlib, sys, csv, datetime, json

def _read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = f.read().strip()
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        objs = []
        buf = ""
        for line in data.splitlines():
            line = line.strip()
            if not line:
                continue
            buf += line
            try:
                objs.append(json.loads(buf))
                buf = ""
            except json.JSONDecodeError:
                continue
        return objs[-1] if objs else {}

def main():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--metrics")
    p.add_argument("--history")
    p.add_argument("--label")
    p.add_argument("pos", nargs="*")
    args, _ = p.parse_known_args()

    metrics = args.metrics
    history = args.history
    trend_png = None

    if not metrics or not history:
        if len(args.pos) >= 2:
            inp = pathlib.Path(args.pos[0])
            metrics = str(inp if inp.suffix == ".json" else inp / "metrics.json")
            history = args.pos[1]
            if len(args.pos) >= 3:
                trend_png = args.pos[2]
        else:
            print("[rollup] need --metrics <json> and --history <csv>", file=sys.stderr)
            return 2

    mpath = pathlib.Path(metrics)
    hpath = pathlib.Path(history)
    if not mpath.exists():
        print(f"[rollup] metrics not found: {mpath}", file=sys.stderr)
        return 2
    hpath.parent.mkdir(parents=True, exist_ok=True)

    new = not hpath.exists()
    if new:
        with open(hpath, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(["timestamp","total","passed","failed","accuracy","metrics_path","label"])

    d = _read_json(mpath)
    total = d.get("total") or d.get("n_total") or d.get("count") or 0
    passed = d.get("passed") or d.get("n_passed") or d.get("correct") or d.get("success") or 0
    failed = d.get("failed") or d.get("n_failed") or (total - passed if total else 0)
    acc = d.get("accuracy") or d.get("acc") or (passed/total if total else 0.0)

    with open(hpath, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z",
            total, passed, failed, round(acc,6), str(mpath), args.label or ""
        ])

    if trend_png:
        pathlib.Path(trend_png).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(trend_png).write_bytes(b"")

    print(f"[rollup] ok: {hpath} updated; total={total} passed={passed} failed={failed} acc={round(acc,6)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
