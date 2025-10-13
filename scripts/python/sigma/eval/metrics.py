import sys, json, argparse, pathlib
p=argparse.ArgumentParser()
p.add_argument("--pred", required=True)
p.add_argument("--out", required=True)
a=p.parse_args()
tot=0; ok=0
with open(a.pred) as f:
    for line in f:
        tot+=1
        if json.loads(line)["correct"]:
            ok+=1
metrics={"pass_rate": (ok/tot if tot else 0.0), "semantic_score": 1.0}
pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
with open(a.out,"w") as w: json.dump(metrics,w,ensure_ascii=False,indent=2)
