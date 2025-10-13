#!/usr/bin/env python3
import sys,csv,statistics
h=sys.argv[1]; o=sys.argv[2]
rows=[]
with open(h) as f:
    r=csv.DictReader(f)
    for row in r:
        if row.get("label","").startswith("t2000_"):
            rows.append(row)
by={}
for r in rows:
    k=r.get("class","all")
    by.setdefault(k,[]).append(float(r["pass_rate"]))
with open(o,"w") as f:
    w=csv.writer(f,delimiter='\t')
    w.writerow(["class","mean_pass_rate","std","n"])
    for k,v in sorted(by.items()):
        m=statistics.fmean(v)
        s=statistics.pstdev(v) if len(v)>1 else 0.0
        w.writerow([k,round(m,4),round(s,4),len(v)])
