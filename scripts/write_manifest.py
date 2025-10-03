#!/usr/bin/env python3
import argparse, csv, json, math, os, re, sys

def count_rows_tsv(path):
    if not os.path.isfile(path): return None
    with open(path, 'r', encoding='utf-8') as f:
        return max(sum(1 for _ in f) - 1, 0)

def read_delta_pp(csv_path):
    if not os.path.isfile(csv_path): return None
    with open(csv_path, 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for i,row in enumerate(r, start=1):
            keys = {k.strip().lower():k for k in row.keys()}
            for cand in ("delta_pp","delta","delta_pp_pct","delta_percent"):
                if cand in keys:
                    try:
                        return float(row[keys[cand]])
                    except: pass
            break
    return None

def read_pass_rate(stab_path):
    if not os.path.isfile(stab_path): return None
    passes=fails=0
    with open(stab_path,'r',encoding='utf-8') as f:
        header=f.readline()
        for line in f:
            s=line.strip().lower()
            if not s: continue
            if re.search(r'(^|[\t, ;])pass([,\t ;]|$)', s): passes+=1
            elif re.search(r'(^|[\t, ;])fail([,\t ;]|$)', s): fails+=1
    tot=passes+fails
    if tot<=0: return None
    return round(passes/float(tot),6)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--dataset', required=False, default='tests/prompts.tsv')
    p.add_argument('--limit', type=int, default=500)
    p.add_argument('--mode', default='nightly')
    p.add_argument('--model-a', default='')
    p.add_argument('--model-b', default='')
    p.add_argument('--out', default='artifacts/manifest.json')
    args=p.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    manifest={}
    rows=count_rows_tsv(args.dataset)
    if rows is not None:
        manifest['rows']=int(min(rows, max(args.limit,0)))
    dpp=read_delta_pp('artifacts/summary/ab_diff.csv')
    if dpp is not None:
        manifest['delta_pp']=float(dpp)
    pr=read_pass_rate('artifacts/summary/stability.tsv')
    if pr is not None:
        manifest['pass_rate']=float(pr)
    manifest['mode']=args.mode
    if args.model_a if hasattr(args,'model_a') else args.model_a: pass
    if args.model_a: manifest['model_a']=args.model_a
    if args.model_b: manifest['model_b']=args.model_b
    with open(args.out,'w',encoding='utf-8') as f:
        json.dump(manifest,f,ensure_ascii=False,indent=2)
    print(args.out)

if __name__=='__main__': main()
