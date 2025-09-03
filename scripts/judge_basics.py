import json, pathlib, re, glob

# 1) карта ожидаемых ответов (минимум на детерминируемые тесты)
EXPECTED = {
  "T1": "1290",            # 1234+56
  "T2": "333",             # 987-654
  "T3": str(37*18-29*17),
  "T4": str(3*3600 + 25*60 + 40),
  "T5": "5",
  "T6": "Париж",
  "T7": str(12-7),
  "T9": str(12345+67890),
  "T10": "3 9 15 27",
  "T12": str(int(2.5*1000)),
  "T14": "да",
  "T15": "tree",
  "T16": "9",
  "T17": "3",
  "T18": str(int((10+20+30+40)/4)),
  "T19": "10",
  "T21": "ток",
  "T22": "да",
  "T23": "бонон",
  "T24": "солнце луна"
}

root = pathlib.Path("artifacts/reports")
rows = []
passed = 0
total = 0

def norm(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    return s

# Берём только основные запуски T1..T24 (без _r#)
for meta in sorted(glob.glob(str(root/"T*"/"meta.json"))):
    test_id = pathlib.Path(meta).parent.name
    if "_r" in test_id:  # пропускаем повторы
        continue
    total += 1
    exp = EXPECTED.get(test_id)
    res = pathlib.Path(meta).with_name("response.txt").read_text(encoding="utf-8", errors="ignore")
    first = res.splitlines()[0] if res else ""
    got = norm(first.lower())
    ok = None
    if exp is None:
        verdict = "SKIP"
        ok = False
    else:
        verdict = "PASS" if got == norm(exp.lower()) else "FAIL"
        ok = (verdict == "PASS")
    if ok:
        passed += 1
    rows.append((test_id, exp if exp is not None else "-", first.strip(), verdict))

out_dir = pathlib.Path("artifacts/summary")
out_dir.mkdir(parents=True, exist_ok=True)
tsv = out_dir/"judgement.tsv"
tsv.write_text(
    "test\texpected\tgot\tverdict\n" + "\n".join(f"{t}\t{e}\t{g}\t{v}" for t,e,g,v in rows),
    encoding="utf-8"
)
(md := out_dir/"judgement.md").write_text(
    "# Judgement\n\n"
    f"Всего тестов: {total}\n\n"
    f"Покрыто чекером: {sum(1 for t, e, g, v in rows if e!='-')}\n\n"
    f"PASS: {passed}\nFAIL: {sum(1 for t,e,g,v in rows if v=='FAIL')}\nSKIP: {sum(1 for t,e,g,v in rows if v=='SKIP')}\n\n",
    encoding="utf-8"
)
print(f"OK -> {tsv}\nOK -> {md}")
