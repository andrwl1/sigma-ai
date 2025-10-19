import sys, json, csv, argparse, pathlib, datetime
p=argparse.ArgumentParser()
p.add_argument("--metrics", required=True)
p.add_argument("--history", required=True)
p.add_argument("--label", required=True)
a=p.parse_args()
with open(a.metrics) as f: m=json.load(f)
pathlib.Path(a.history).parent.mkdir(parents=True, exist_ok=True)
hdr=["ts","label","pass_rate","semantic_score"]
rows=[]
try:
    with open(a.history,newline='') as f: rows=list(csv.reader(f))
except FileNotFoundError: rows=[hdr]
rows.append([datetime.datetime.utcnow().isoformat(timespec="seconds")+"Z",a.label,str(m["pass_rate"]),str(m["semantic_score"])])
with open(a.history,"w",newline='') as f: csv.writer(f).writerows(rows)
