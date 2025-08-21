from pathlib import Path
import json, datetime

today = datetime.date.today().isoformat()
reports = Path("reports"); metrics_p = reports / "metrics.json"

status_line = "UNKNOWN"
reasons = []
loss_last = None
acc_last = None

if metrics_p.exists():
    m = json.loads(metrics_p.read_text())
    st = m.get("status", {})
    if isinstance(st, dict) and "pass" in st:
        status_line = "PASS" if st.get("pass") else "FAIL"
        reasons = st.get("reasons", [])
    stats = m.get("stats", {})
    if isinstance(stats.get("loss"), dict):
        loss_last = stats["loss"].get("last")
    for k in ("accuracy", "acc"):
        if isinstance(stats.get(k), dict):
            acc_last = stats[k].get("last")
            if acc_last is not None:
                break

# Fallback, если статуса нет
if status_line == "UNKNOWN":
    pass_fallback = True
    if loss_last is not None and loss_last > 0.5:
        pass_fallback = False
        reasons.append("loss_last > 0.5")
    if acc_last is not None and acc_last < 0.8:
        pass_fallback = False
        reasons.append("accuracy_last < 0.8")
    status_line = "PASS" if pass_fallback else "FAIL"

# последний bundle
bundle_name = ""
bd = Path("bundle")
if bd.exists():
    bundles = sorted(bd.glob("bundle_*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if bundles:
        bundle_name = bundles[0].name

# таймлайн
tl = Path("archive") / "TIMELINE.md"
tl.parent.mkdir(exist_ok=True)
if not tl.exists():
    tl.write_text("# ∑AI Timeline\n\nDate | Status | Loss(last) | Acc(last) | Bundle | Reasons\n---|---|---:|---:|---|---\n")
line = f"{today} | {status_line} | {'' if loss_last is None else loss_last} | {'' if acc_last is None else acc_last} | {bundle_name} | {('; '.join(reasons)) if reasons else ''}\n"
with tl.open("a") as f:
    f.write(line)

# печать краткого JSON (удобно для отладки)
print(json.dumps({
    "date": today,
    "status": status_line,
    "reasons": reasons,
    "loss_last": loss_last,
    "acc_last": acc_last,
    "bundle": bundle_name,
    "timeline": str(tl)
}, indent=2))
