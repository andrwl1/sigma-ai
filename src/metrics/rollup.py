import argparse, csv, json, pathlib
import matplotlib.pyplot as plt

def read_history(path):
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            for k in ['pass_rate', 'bleu', 'rouge_l', 'semantic_score']:
                row[k] = float(row[k])
            rows.append(row)
    return rows

def save_trend(xs, ys, out_png, title, ylabel):
    plt.figure()
    plt.plot(xs, ys, marker='o')
    plt.title(title)
    plt.xlabel('step')
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(out_png, bbox_inches='tight', dpi=150)
    plt.close()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--history', required=True)
    ap.add_argument('--outdir', required=True)
    args = ap.parse_args()

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = read_history(args.history)
    xs = list(range(1, len(rows) + 1))
    pr = [r['pass_rate'] for r in rows]
    bleu = [r['bleu'] for r in rows]
    rouge = [r['rouge_l'] for r in rows]
    sem = [r['semantic_score'] for r in rows]

    save_trend(xs, pr, outdir / 'passrate_trend.png', 'Pass Rate Trend', 'pass_rate')
    save_trend(xs, bleu, outdir / 'trend_bleu.png', 'BLEU Trend', 'BLEU')
    save_trend(xs, rouge, outdir / 'trend_rouge.png', 'ROUGE-L Trend', 'ROUGE-L')
    save_trend(xs, sem, outdir / 'semantic_drift.png', 'Semantic Drift', 'semantic_score')

    with open(outdir / 'metrics_latest.json', 'w', encoding='utf-8') as f:
        json.dump(rows[-1] if rows else {}, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
