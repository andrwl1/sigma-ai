from pathlib import Path
import json, csv, datetime, re

now = datetime.datetime.now().isoformat(timespec="seconds")

reports = Path("reports"); reports.mkdir(exist_ok=True)
metrics_p = reports / "metrics.json"

status = "UNKNOWN"; loss_last = ""; acc_last = ""; bundle = ""

# 1) читаем последние метрики (для loss/acc и, если есть, базового статуса)
if metrics_p.exists():
    m = json.loads(metrics_p.read_text())
    st = m.get("status", {})
    if isinstance(st, dict) and "pass" in st:
        status = "PASS" if st.get("pass") else "FAIL"
    stats = m.get("stats", {})
    if isinstance(stats.get("loss"), dict):
        v = stats["loss"].get("last"); loss_last = "" if v is None else v
    for k in ("accuracy","acc"):
        if isinstance(stats.get(k), dict):
            v = stats[k].get("last")
            if v is not None: acc_last = v; break

# 2) ищем последний bundle (и пригодится для сверки)
bd = Path("bundle")
if bd.exists():
    bs = sorted(bd.glob("bundle_*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if bs: bundle = bs[0].name

# 3) статус берём из таймлайна (источник истины)
tl = Path("archive") / "TIMELINE.md"
if tl.exists():
    lines = [ln.strip() for ln in tl.read_text().splitlines() if ln.strip() and not ln.startswith("#") and not ln.startswith("---")]
    if lines:
        last = lines[-1]  # формат: Date | Status | Loss(last) | Acc(last) | Bundle | Reasons
        parts = [p.strip() for p in last.split("|")]
        if len(parts) >= 2:
            tl_status = parts[1]
            if tl_status in ("PASS","FAIL"):
                status = tl_status

# 4) если статуса всё ещё нет — делаем простой fallback (как в mark_day.py)
if status == "UNKNOWN":
    pass_fb = True
    try:
        if loss_last != "" and float(loss_last) > 0.5: pass_fb = False
        if acc_last  != "" and float(acc_last)  < 0.8: pass_fb = False
    except Exception:
        pass
    status = "PASS" if pass_fb else "FAIL"

# 5) пишем строку в history.csv
hist = reports / "history.csv"
write_header = not hist.exists()
with hist.open("a", newline="") as f:
    w = csv.writer(f)
    if write_header:
        w.writerow(["timestamp","status","loss_last","acc_last","bundle"])
    w.writerow([now, status, loss_last, acc_last, bundle])

print(f"history: appended -> {hist}")
