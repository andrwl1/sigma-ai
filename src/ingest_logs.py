import re, json, csv
from pathlib import Path
from datetime import datetime

logs = Path("logs")
logs.mkdir(exist_ok=True)

def latest(pattern: str):
    return sorted(logs.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)

# 1) Если уже есть CSV — используем его
csvs = latest("*.csv")
if csvs:
    print(f"ingest: found csv -> {csvs[0]}")
    raise SystemExit(0)

rows = []

# 2) JSON / JSONL
json_files = latest("*.json") + latest("*.jsonl")
for jf in json_files:
    try:
        if jf.suffix == ".jsonl":
            for i, line in enumerate(jf.read_text().splitlines(), 1):
                line = line.strip()
                if not line:
                    continue
                o = json.loads(line)
                epoch = o.get("epoch") or o.get("step") or i
                loss = o.get("loss")
                acc  = o.get("accuracy") or o.get("acc")
                if loss is None:
                    continue
                rows.append({
                    "epoch": int(epoch),
                    "loss": float(loss),
                    **({"accuracy": float(acc)} if acc is not None else {})
                })
        else:  # .json
            data = json.loads(jf.read_text())
            if isinstance(data, list):
                for i, o in enumerate(data, 1):
                    epoch = o.get("epoch") or o.get("step") or i
                    loss = o.get("loss")
                    acc  = o.get("accuracy") or o.get("acc")
                    if loss is None:
                        continue
                    rows.append({
                        "epoch": int(epoch),
                        "loss": float(loss),
                        **({"accuracy": float(acc)} if acc is not None else {})
                    })
            elif isinstance(data, dict):
                # формат {"epoch":[...], "loss":[...], "accuracy":[...]} тоже поддержим
                epochs = data.get("epoch") or data.get("step")
                losses = data.get("loss")
                if isinstance(epochs, list) and isinstance(losses, list):
                    accs = data.get("accuracy") or data.get("acc") or [None] * len(losses)
                    for i, (e, l, a) in enumerate(zip(epochs, losses, accs), 1):
                        rows.append({
                            "epoch": int(e or i),
                            "loss": float(l),
                            **({"accuracy": float(a)} if a is not None else {})
                        })
    except Exception:
        pass
    if rows:
        break

# 3) TXT / LOG при помощи regex
if not rows:
    txts = latest("*.txt") + latest("*.log")
    if txts:
        src = txts[0]
        patts = [
            re.compile(r"epoch[:\s]*(\d+)[^\d\n]+loss[:\s]*([0-9]*\.?[0-9]+)", re.I),
            re.compile(r"step[:\s]*(\d+)[^\d\n]+loss[:\s]*([0-9]*\.?[0-9]+)", re.I),
            re.compile(r"\be(?:poch)?\s*(\d+)\b[^\n]*?loss[^\d]*([0-9]*\.?[0-9]+)", re.I),
        ]
        acc_patts = [re.compile(r"acc(?:uracy)?[:\s]*([0-9]*\.?[0-9]+)", re.I)]

        for i, line in enumerate(src.read_text().splitlines(), 1):
            epoch = loss = acc = None
            for p in patts:
                m = p.search(line)
                if m:
                    epoch = int(m.group(1))
                    loss = float(m.group(2))
                    break
            if epoch is None and loss is None:
                m = re.search(r"loss[:=\s]*([0-9]*\.?[0-9]+)", line, re.I)
                if m:
                    epoch = i
                    loss = float(m.group(1))
            if epoch is None or loss is None:
                continue
            for ap in acc_patts:
                am = ap.search(line)
                if am:
                    try:
                        acc = float(am.group(1))
                    except Exception:
                        pass
                    break
            rows.append({
                "epoch": epoch,
                "loss": loss,
                **({"accuracy": acc} if acc is not None else {})
            })

if not rows:
    print("ingest: no suitable logs")
    raise SystemExit(0)

rows.sort(key=lambda r: r["epoch"])
out = logs / f"ingested_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["epoch", "loss", "accuracy"])
    w.writeheader()
    for r in rows:
        w.writerow({
            "epoch": r["epoch"],
            "loss": r["loss"],
            "accuracy": r.get("accuracy")
        })
print(f"ingest: written -> {out}")
