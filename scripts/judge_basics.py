import pathlib, re, glob

EXPECTED = {
  "T1": 1290, "T2": 333, "T3": 37*18-29*17, "T4": 3*3600+25*60+40,
  "T5": 5, "T6": "париж", "T7": 5, "T8": 12, "T9": 12345+67890,
  "T10": [3,9,15,27], "T12": 2500, "T13": 8, "T14": "да", "T15": "tree",
  "T16": 9, "T17": 3, "T18": 25, "T19": 10, "T21": "ток", "T22": "да",
  "T23": "бонон", "T24": "солнце луна",
}

YES = {"да","yes","y","true","истина"}
NO  = {"нет","no","n","false","ложь"}

ansi_re = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

def strip_ansi(s: str) -> str:
    return ansi_re.sub("", s)

def norm(s: str) -> str:
    s = strip_ansi(s)
    s = "".join(ch for ch in s if ch.isprintable()).strip().lower()
    s = re.sub(r"[«»\"'`.,!?;:]+$", "", s)
    s = re.sub(r"\s+", " ", s)
    return s

root = pathlib.Path("artifacts/reports")
rows=[]; passed=0; total=0

for meta in sorted(glob.glob(str(root/"T*"/"meta.json"))):
    tid = pathlib.Path(meta).parent.name
    if "_r" in tid: 
        continue
    total += 1
    exp = EXPECTED.get(tid)
    if exp is None:
        rows.append((tid,"-","-","SKIP"))
        continue

    resp = (pathlib.Path(meta).with_name("response.txt")
            .read_text(encoding="utf-8", errors="ignore"))
    line_raw = resp.splitlines()[0] if resp else ""
    got = norm(line_raw)

    verdict="FAIL"
    if isinstance(exp,int):
        m = re.findall(r"-?\d+", got)
        if m and int(m[-1]) == exp:
            verdict="PASS"
    elif isinstance(exp,list):
        nums=[int(x) for x in re.findall(r"-?\d+", got)]
        if nums==exp: verdict="PASS"
    elif isinstance(exp,str):
        if exp=="париж":
            verdict = "PASS" if got in {"париж","paris"} else "FAIL"
        elif exp in YES:
            verdict = "PASS" if got in YES else "FAIL"
        elif exp in NO:
            verdict = "PASS" if got in NO else "FAIL"
        elif exp=="солнце луна":
            verdict = "PASS" if got=="солнце луна" else "FAIL"
        else:
            verdict = "PASS" if got==exp else "FAIL"

    if verdict=="PASS": passed+=1
    rows.append((tid,str(exp),got,verdict))

out=pathlib.Path("artifacts/summary"); out.mkdir(parents=True, exist_ok=True)
(out/"judgement.tsv").write_text(
 "test\texpected\tgot\tverdict\n"+"\n".join(f"{t}\t{e}\t{g}\t{v}" for t,e,g,v in rows),
 encoding="utf-8")
(out/"judgement.md").write_text(
 "# Judgement\n\n"
 f"Всего тестов: {total}\n\n"
 f"Покрыто чекером: {sum(1 for t,e,g,v in rows if e!='-')}\n\n"
 f"PASS: {sum(1 for t,e,g,v in rows if v=='PASS')}\n"
 f"FAIL: {sum(1 for t,e,g,v in rows if v=='FAIL')}\n"
 f"SKIP: {sum(1 for t,e,g,v in rows if v=='SKIP')}\n\n",
 encoding="utf-8")
print("OK -> judgement.tsv, judgement.md")
