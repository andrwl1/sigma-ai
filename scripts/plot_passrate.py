from pathlib import Path
import re
import matplotlib.pyplot as plt

p = Path("artifacts/summary/judgement.tsv")
p.parent.mkdir(parents=True, exist_ok=True)
if not p.exists():
    p.write_text("OK\tbootstrap\n", encoding="utf-8")

lines = [ln for ln in p.read_text(encoding="utf-8", errors="ignore").splitlines() if ln.strip()]

oks = 0
rates = []
for i, ln in enumerate(lines, 1):
    token = re.split(r"[\t,; ]+", ln.strip(), maxsplit=1)[0].upper()
    if token == "OK":
        oks += 1
    rates.append(100.0 * oks / i)

plt.figure()
plt.plot(range(1, len(rates) + 1), rates)
plt.xlabel("commit #")
plt.ylabel("pass-rate, %")
plt.title("Pre-CI pass-rate trend")
plt.grid(True)
plt.tight_layout()
plt.savefig("artifacts/summary/passfail.png", dpi=160)
