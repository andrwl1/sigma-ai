import pandas as pd, matplotlib.pyplot as plt, os
os.makedirs("artifacts/summary", exist_ok=True)
p="artifacts/summary/judgement.tsv"
if not os.path.exists(p):
    with open(p,"w") as f: f.write("OK\tbootstrap\n")
df = pd.read_csv(p, sep="\t", header=None, names=["status","note"])
df["ok"]= (df["status"]=="OK").astype(int)
df["cum_pass_rate"]= df["ok"].expanding().mean()*100
plt.figure()
plt.plot(df.index+1, df["cum_pass_rate"])
plt.xlabel("commit #"); plt.ylabel("pass-rate, %"); plt.title("Pre-CI pass-rate trend")
plt.grid(True); plt.tight_layout(); plt.savefig("artifacts/summary/passfail.png", dpi=160)
