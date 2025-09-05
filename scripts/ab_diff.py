import pandas as pd
import pathlib
import sys
from textwrap import shorten

# ---------- utils ----------
def load_df(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep="\t", dtype=str).fillna("")

def pick(cols, candidates):
    m = {c.lower(): c for c in cols}
    for x in candidates:
        if x in m: 
            return m[x]
    # если ничего не нашли — берём первый столбец
    return cols[0]

def verdict_col(df: pd.DataFrame) -> str:
    return pick(df.columns, ["verdict","result","status","pass"])

def id_col(df: pd.DataFrame) -> str:
    return pick(df.columns, ["test","id","test_id","prompt_id","case_id"])

def got_col(df: pd.DataFrame) -> str:
    return pick(df.columns, ["got","answer","output","prediction"])

def pass_mask(series: pd.Series) -> pd.Series:
    return series.str.upper().isin(["PASS","PASSED","1","TRUE","YES"])

# ---------- main ----------
def main() -> int:
    local_j = "artifacts/local/judgement.tsv"
    cloud_j = "artifacts/cloud/judgement.tsv"

    dfl = load_df(local_j)
    dfc = load_df(cloud_j)

    lid, lver, lgot = id_col(dfl), verdict_col(dfl), got_col(dfl)
    cid, cver, cgot = id_col(dfc), verdict_col(dfc), got_col(dfc)

    lf = dfl[[lid, lver, lgot]].rename(columns={lid:"id", lver:"ver_local", lgot:"got_local"})
    cf = dfc[[cid, cver, cgot]].rename(columns={cid:"id", cver:"ver_cloud", cgot:"got_cloud"})

    merged = lf.merge(cf, on="id", how="outer", indicator=True)

    # различия по вердикту или по ответу
    diff_mask = (
        (merged["ver_local"].fillna("") != merged["ver_cloud"].fillna("")) |
        (merged["got_local"].fillna("")  != merged["got_cloud"].fillna(""))
    )
    diffs = merged[diff_mask].copy()

    # аккуратный вид в MD
    def clip(x): return shorten(str(x), width=120, placeholder="…")
    if not diffs.empty:
        diffs["got_local"] = diffs["got_local"].map(clip)
        diffs["got_cloud"] = diffs["got_cloud"].map(clip)

    out_md = pathlib.Path("artifacts/summary/ab_diff.md")
    lines = [
        "# A/B Diff (local vs cloud)",
        "",
        f"Всего кейсов: {len(merged)}",
        f"Расхождений: {len(diffs)}",
        ""
    ]
    if diffs.empty:
        lines.append("✅ Различий не обнаружено.")
    else:
        # короткая сводка по типам изменений
        summary = {
            "verdict_only": ((merged["ver_local"] != merged["ver_cloud"]) &
                             (merged["got_local"] == merged["got_cloud"])).sum(),
            "answer_only":  ((merged["ver_local"] == merged["ver_cloud"]) &
                             (merged["got_local"] != merged["got_cloud"])).sum(),
            "both":         ((merged["ver_local"] != merged["ver_cloud"]) &
                             (merged["got_local"] != merged["got_cloud"])).sum(),
        }
        lines += [
            "## Сводка по типам",
            f"- Только вердикт отличается: {summary['verdict_only']}",
            f"- Только ответ отличается:  {summary['answer_only']}",
            f"- И вердикт и ответ:        {summary['both']}",
            "",
            "## Примеры различий (первые 50)",
            "",
            diffs.head(50).to_markdown(index=False)
        ]

    out_md.write_text("\n".join(lines), encoding="utf-8")
    print("OK:", out_md)

    # если есть различия — вернуть код 1 (для «охранника»)
    return 1 if len(diffs) > 0 else 0

if __name__ == "__main__":
    sys.exit(main())
