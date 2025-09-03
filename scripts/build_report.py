import json, os, glob, datetime, pathlib
root = pathlib.Path("artifacts/reports")
rows = []
for meta in sorted(glob.glob(str(root/"T*"/"meta.json"))):
    with open(meta, 'r', encoding='utf-8') as f:
        m = json.load(f)
    test = m["test"]
    model = m["model"]
    ts = m["timestamp_utc"]
    req = pathlib.Path(meta).with_name("request.txt").read_text(encoding="utf-8").strip()
    res = pathlib.Path(meta).with_name("response.txt").read_text(encoding="utf-8").strip()
    rows.append((test, model, ts, req, res))

out_dir = pathlib.Path("artifacts/summary")
out_dir.mkdir(parents=True, exist_ok=True)
md = ["# Автоотчёт по локальному прогонам",
      "",
      f"_Сгенерировано: {datetime.datetime.utcnow().isoformat()}Z_",
      "",
      "| Тест | Модель | Время (UTC) | Промпт | Ответ (первая строка) |",
      "|-----:|:------:|:------------|--------|------------------------|"]
for t, model, ts, req, res in rows:
    first = res.splitlines()[0] if res else ""
    req_short = (req[:120] + "…") if len(req) > 120 else req
    first_short = (first[:120] + "…") if len(first) > 120 else first
    md.append(f"| {t} | {model} | {ts} | {req_short.replace('|','\\|')} | {first_short.replace('|','\\|')} |")

path = out_dir/"report.md"
path.write_text("\n".join(md), encoding="utf-8")
print(f"OK report -> {path}")
