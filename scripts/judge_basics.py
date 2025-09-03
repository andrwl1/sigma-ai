import pathlib, re, glob

# Ожидаемые ответы (только для детерминируемых)
EXPECTED = {
  "T1": 1290,            # числа — как int
  "T2": 333,
  "T3": 37*18-29*17,
  "T4": 3*3600 + 25*60 + 40,
  "T5": 5,
  "T6": "париж",         # допускаем 'paris'
  "T7": 5,
  "T8": 12,              # сумма колонки A: 2+4+6
  "T9": 12345+67890,
  "T10": [3,9,15,27],    # список чисел по порядку
  # T11 — день недели — SKIP (зависит от календарной логики)
  "T12": 2500,
  "T13": 8,              # 3 друга + пятеро = 8
  "T14": "да",           # допускаем yes/true
  "T15": "tree",
  "T16": 9,
  "T17": 3,
  "T18": 25,
  "T19": 10,
  "T20": None,           # логика — SKIP
  "T21": "ток",
  "T22": "да",
  "T23": "бонон",        # 'банан' -> 'бонон'
  "T24": "солнце луна",
}

YES = {"да","yes","y","true","истина"}
NO  = {"нет","no","n","false","ложь"}

def norm_text(s:str)->str:
    s = s.strip().lower()
    s = re.sub(r"^ответ[:\s-]*", "", s)
    s = re.sub(r"[«»\"'`]", "", s)
    s = re.sub(r"[.,!?;:]+$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

def first_line(resp:str)->str:
    return resp.splitlines()[0] if resp else ""

def ints_in(s:str):
    return [int(x) for x in re.findall(r"-?\d+", s)]

root = pathlib.Path("artifacts/reports")
rows, passed, total = [], 0, 0

for meta in sorted(glob.glob(str(root/"T*"/"meta.json"))):
    test_id = pathlib.Path(meta).parent.name
    if "_r" in test_id:     # игнорируем повторы серий
        continue
    total += 1
    exp = EXPECTED.get(test_id, None)
    # SKIP если нет стратегии проверки
    if exp is None:
        rows.append((test_id, "-", "-", "SKIP"))
        continue

    res = (pathlib.Path(meta).with_name("response.txt")
           .read_text(encoding="utf-8", errors="ignore"))
    got_raw = first_line(res)
    got = norm_text(got_raw)

    verdict = "FAIL"

    # Числовые ответы (int)
    if isinstance(exp, int):
        got_nums = ints_in(got)
        if got_nums and got_nums[0] == exp:
            verdict = "PASS"

    # Списки чисел
    elif isinstance(exp, list) and all(isinstance(x,int) for x in exp):
        got_nums = ints_in(got)
        if got_nums == exp:
            verdict = "PASS"

    # Строки (да/нет/слово/фраза)
    elif isinstance(exp, str):
        g = got
        e = norm_text(exp)

        # да/нет
        if e in YES:
            verdict = "PASS" if g in YES else "FAIL"
        elif e in NO:
            verdict = "PASS" if g in NO else "FAIL"
        # 'париж' или 'paris'
        elif e == "париж":
            verdict = "PASS" if g in {"париж","paris"} else "FAIL"
        # остальное — точное совпадение после нормализации
        else:
            verdict = "PASS" if g == e else "FAIL"

    if verdict == "PASS":
        passed += 1

    exp_str = str(exp) if exp is not None else "-"
    rows.append((test_id, exp_str, got_raw.strip(), verdict))

out_dir = pathlib.Path("artifacts/summary")
out_dir.mkdir(parents=True, exist_ok=True)

# TSV
tsv = out_dir/"judgement.tsv"
tsv.write_text(
    "test\texpected\tgot\tverdict\n" +
    "\n".join(f"{t}\t{e}\t{g}\t{v}" for t,e,g,v in rows),
    encoding="utf-8"
)

# MD сводка
md = out_dir/"judgement.md"
md.write_text(
    "# Judgement\n\n"
    f"Всего тестов: {total}\n\n"
    f"Покрыто чекером: {sum(1 for t,e,g,v in rows if e!='-')}\n\n"
    f"PASS: {sum(1 for t,e,g,v in rows if v=='PASS')}\n"
    f"FAIL: {sum(1 for t,e,g,v in rows if v=='FAIL')}\n"
    f"SKIP: {sum(1 for t,e,g,v in rows if v=='SKIP')}\n\n",
    encoding="utf-8"
)

print(f"OK -> {tsv}\nOK -> {md}")
