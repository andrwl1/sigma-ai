import sys, json, csv, argparse, pathlib
p=argparse.ArgumentParser()
p.add_argument("--tests", required=True)
p.add_argument("--out", required=True)
a=p.parse_args()
pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
with open(a.tests, newline='') as f, open(a.out, 'w') as w:
    r=csv.DictReader(f, delimiter='\t')
    for row in r:
        pred=row['expected']
        w.write(json.dumps({"prompt":row['prompt'],"expected":row['expected'],"pred":pred,"correct":pred==row['expected']}, ensure_ascii=False)+"\n")
