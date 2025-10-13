import csv, argparse
import matplotlib.pyplot as plt
p=argparse.ArgumentParser()
p.add_argument("--history", required=True)
p.add_argument("--out", required=True)
a=p.parse_args()
x=[]; y=[]
with open(a.history) as f:
    r=csv.DictReader(f)
    for row in r:
        if row["label"].startswith("t2000_"):
            x.append(row["ts"]); y.append(float(row["pass_rate"]))
plt.figure(); plt.plot(range(len(y)), y, marker="o"); plt.xlabel("run"); plt.ylabel("pass_rate"); plt.title("T2000 trend")
plt.savefig(a.out, bbox_inches="tight")
