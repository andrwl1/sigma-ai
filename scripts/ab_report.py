import pandas as pd
import pathlib

def load_df(path):
    return pd.read_csv(path, sep="\t", dtype=str).fillna("")

def pass_rate(df):
    verdict_col = next(c for c in df.columns if c.lower() in ["verdict","result","status","pass"])
    passed = df[verdict_col].str.upper().isin(["PASS","PASSED","1","TRUE","YES"]).sum()
    total = len(df)
    return passed, total, passed/total if total else 0

def main():
    local_j = "artifacts/local/judgement.tsv"
    cloud_j = "artifacts/cloud/judgement.tsv"

    dfl = load_df(local_j)
    dfc = load_df(cloud_j)

    pl, tl, rl = pass_rate(dfl)
    pc, tc, rc = pass_rate(dfc)

    out = pathlib.Path("artifacts/summary/ab_report.md")
    out.write_text(
f"""# A/B Report

## Local
- Passed: {pl}/{tl}
- Rate: {rl:.2%}

## Cloud
- Passed: {pc}/{tc}
- Rate: {rc:.2%}

## Δ Difference
- Abs: {pc-pl}
- Rate Δ: {(rc-rl):.2%}
"""
    )
    print("OK:", out)

if __name__ == "__main__":
    main()
