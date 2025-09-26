#!/usr/bin/env python3
import argparse,csv,hashlib,json,os,statistics,subprocess,time
def fnum(x):
    try: return float(x)
    except: return 0.0
def ibool(x):
    v=str(x).strip().lower()
    if v in ("1","true","t","yes","y"): return 1
    if v in ("0","false","f","no","n",""): return 0
    try: return int(v)
    except: return 0
def p95(xs):
    if not xs: return 0.0
    xs=sorted(xs); k=max(0,int(round(0.95*(len(xs)-1))))
    return float(xs[k])
p=argparse.ArgumentParser()
p.add_argument("--dataset",required=True)
p.add_argument("--limit",type=int,required=True)
p.add_argument("--mode",required=True)
p.add_argument("--model-a",required=True)
p.add_argument("--model-b",required=True)
p.add_argument("--runner",default="local")
p.add_argument("--csv",default="artifacts/summary/ab_diff.csv")
p.add_argument("--out",default="artifacts/manifest.json")
a=p.parse_args()
os.makedirs("artifacts",exist_ok=True)
with open(a.dataset,"rb") as f:
    dataset_sha=hashlib.sha256(f.read()).hexdigest()
deltas=[]; eq=0; rows=0
with open(a.csv,newline="") as f:
    r=csv.DictReader(f)
    for row in r:
        rows+=1
        deltas.append(fnum(row.get("delta_pp","0")))
        eq+=ibool(row.get("equal","0"))
pass_rate=(eq/rows) if rows else 0.0
mean=statistics.mean(deltas) if deltas else 0.0
p95v=p95(deltas)
commit=subprocess.check_output(["git","rev-parse","HEAD"]).decode().strip()
branch=subprocess.check_output(["git","rev-parse","--abbrev-ref","HEAD"]).decode().strip()
ts=int(time.time()*1000)
manifest={
  "commit":commit,"branch":branch,"run_id":str(ts),"timestamp":ts,"runner":a.runner,
  "dataset_sha":dataset_sha,"limit":a.limit,"model_a":a.model_a,"model_b":a.model_b,
  "mode":a.mode,"rows":rows,"pass_rate":pass_rate,"delta_pp_mean":mean,"delta_pp_p95":p95v
}
with open(a.out,"w") as f: json.dump(manifest,f,indent=2,sort_keys=True)
print(a.out)
