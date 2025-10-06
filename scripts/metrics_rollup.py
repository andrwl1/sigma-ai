import csv, os, datetime, json, matplotlib.pyplot as plt
src="artifacts/t1000/latest/ab_diff_local.csv"
hist="artifacts/t1000/metrics_history.csv"
os.makedirs("artifacts/t1000", exist_ok=True)
rows=0
if os.path.exists(src):
    with open(src,newline="",encoding="utf-8") as f:
        r=csv.reader(f)
        next(r,None)
        data=list(r)
        rows=len(data)
pass_rate=0.0
delta_pp=0.0
today=datetime.date.today().isoformat()
new=[today,rows,pass_rate,delta_pp]
hdr=["date","rows","pass_rate","delta_pp"]
if not os.path.exists(hist):
    with open(hist,"w",newline="",encoding="utf-8") as f: csv.writer(f).writerow(hdr)
with open(hist,"a",newline="",encoding="utf-8") as f: csv.writer(f).writerow(new)
xs=[]; ys=[]
with open(hist,newline="",encoding="utf-8") as f:
    r=csv.DictReader(f)
    for row in r:
        xs.append(row["date"]); ys.append(float(row["pass_rate"]))
plt.figure(figsize=(6,3))
plt.plot(range(len(ys)), ys, "o-")
plt.xticks(range(len(xs)), xs, rotation=45, ha="right")
plt.tight_layout()
plt.savefig("artifacts/t1000/passrate_local.png")
print(f"rollup_ok rows={rows} entries={len(ys)}")
