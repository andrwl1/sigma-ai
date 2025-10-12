import argparse, json, time, csv
from datetime import datetime, timezone
from pathlib import Path
from .adapters import generate
import sacrebleu
import evaluate as hf_eval
from sentence_transformers import SentenceTransformer
import numpy as np

def read_pairs(tsv_path):
    rows=[]
    with open(tsv_path,'r',encoding='utf-8') as f:
        for line in f:
            if not line.strip(): 
                continue
            if '\t' not in line: 
                continue
            p,e = line.rstrip('\n').split('\t',1)
            rows.append((p,e))
    return rows

def pass_rate(pairs, preds):
    ok=0
    for (p,exp),pred in zip(pairs,preds):
        if pred.strip()==exp.strip():
            ok+=1
    return ok/len(pairs) if pairs else 0.0

def compute_bleu(refs, hyps):
    return sacrebleu.corpus_bleu(hyps, [refs]).score/100.0

def compute_rouge_l(refs, hyps):
    rouge = hf_eval.load("rouge")
    res = rouge.compute(predictions=hyps, references=refs, use_aggregator=True)
    return float(res.get("rougeL",0.0))

def compute_cosine(refs, hyps):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    a = model.encode(refs, normalize_embeddings=True)
    b = model.encode(hyps, normalize_embeddings=True)
    sims = (a*b).sum(axis=1)
    return float(np.mean(sims).item())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--tsv',required=True)
    ap.add_argument('--outdir',required=True)
    ap.add_argument('--history',required=True)
    ap.add_argument('--run-id',dest='run_id',default=str(int(time.time())))
    args=ap.parse_args()

    outdir=Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    pairs=read_pairs(args.tsv)
    refs=[e for _,e in pairs]
    hyps=[generate(p) for p,_ in pairs]

    pr=pass_rate(pairs, hyps)
    bleu=compute_bleu(refs, hyps)
    rouge_l=compute_rouge_l(refs, hyps)
    cosine=compute_cosine(refs, hyps)

    ts=datetime.now(timezone.utc).isoformat(timespec='seconds')
    report={'run_id':args.run_id,'timestamp':ts,'pass_rate':pr,'bleu':bleu,'rouge_l':rouge_l,'semantic_score':cosine}

    with open(outdir/'metrics.json','w',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)
    with open(outdir/'metrics_latest.json','w',encoding='utf-8') as f:
        json.dump(report,f,ensure_ascii=False,indent=2)

    hist_path=Path(args.history)
    new_file=not hist_path.exists()
    hist_path.parent.mkdir(parents=True, exist_ok=True)
    with open(hist_path,'a',newline='',encoding='utf-8') as f:
        w=csv.writer(f)
        if new_file:
            w.writerow(['run_id','timestamp','pass_rate','bleu','rouge_l','semantic_score'])
        w.writerow([report['run_id'],report['timestamp'],f"{pr:.6f}",f"{bleu:.6f}",f"{rouge_l:.6f}",f"{cosine:.6f}"])

    print(json.dumps(report,ensure_ascii=False))

if __name__=="__main__":
    main()

