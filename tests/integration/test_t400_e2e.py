import subprocess, re

ANSI = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

def run(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    out = ANSI.sub('', p.stdout or '')
    return p.returncode, out

def test_addition_t26_returns_4():
    # Правильный порядок: ID, промпт, модель
    rc, out = run(["bash", "scripts/run_local_answer.sh", "T26", "2+2? Ответ только числом.", "llama3.1:8b"])
    assert rc in (0, 141, 3), f"unexpected rc={rc}\n{out}"  # 3 = нет текстовых артефактов (тогда тест подскажет, что поправить)
    assert re.search(r"\b4\b", out), f"no '4' in output:\n{out}"
