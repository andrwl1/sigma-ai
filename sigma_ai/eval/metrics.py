import argparse, json, pathlib, datetime, csv, sys
def _read(p):
    with open(p, "r", encoding="utf-8") as f: d=json.load(f)
    total=d.get("total") or d.get("n_total") or d.get("count") or 0
    passed=d.get("passed") or d.get("n_passed") or d.get("correct") or d.get("success") or 0
    failed=d.get("failed") or d.get("n_failed") or (total-passed if total else 0)
    acc=d.get("accuracy") or d.get("acc") or (passed/total if total else 0.0)
    return total, passed, failed, float(acc)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("metrics_path_or_dir"); ap.add_argument("history_csv"); a=ap.parse_args()
    p=pathlib.Path(a.metrics_path_or_dir); m=p if p.suffix==".json" else p/"metrics.json"
    total,passed,failed,acc=_read(m)
    h=pathlib.Path(a.history_csv); h.parent.mkdir(parents=True, exist_ok=True); new=not h.exists()
    with open(h,"a",newline="",encoding="utf-8") as f:
        w=csv.writer(f); 
        if new: w.writerow(["timestamp","total","passed","failed","accuracy","metrics_path"])
        w.writerow([datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z", total, passed, failed, round(acc,6), str(m)])
    print(f"OK {h} total={total} passed={passed} failed={failed} acc={round(acc,6)}")
    return 0
if __name__=="__main__": sys.exit(main())
