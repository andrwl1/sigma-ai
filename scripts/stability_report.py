from pathlib import Path
import matplotlib.pyplot as plt
import csv

summary_dir = Path("artifacts/summary")
summary_dir.mkdir(parents=True, exist_ok=True)

judgement = summary_dir / "judgement.tsv"
passfail_png = summary_dir / "passfail.png"
ab_diff_csv = summary_dir / "ab_diff.csv"

# --- график стабильности ---
if judgement.exists():
    lines = [ln.strip() for ln in judgement.read_text(encoding="utf-8").splitlines() if ln.strip()]
    oks = 0
    rates = []
    for i, ln in enumerate(lines, 1):
        if ln.split("\t")[0].upper() == "OK":
            oks += 1
        rates.append(100.0 * oks / i)

    plt.figure()
    plt.plot(range(1, len(rates) + 1), rates)
    plt.xlabel("commit #")
    plt.ylabel("pass-rate, %")
    plt.title("Pre-CI pass-rate trend")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(passfail_png, dpi=160)
    print(f"[+] trend plot saved to {passfail_png}")
else:
    print("[!] judgement.tsv not found, skipping trend plot")

# --- фиксация расхождений ---
ab_diff = []
for path in summary_dir.glob("ab_diff*.tsv"):
    with path.open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if len(row) >= 3:
                ab_diff.append(row[:3])  # id, expected, actual

if ab_diff:
    with ab_diff_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "expected", "actual"])
        writer.writerows(ab_diff)
    print(f"[+] ab_diff saved to {ab_diff_csv}")
else:
    print("[!] no ab_diff.tsv found, skipping")
