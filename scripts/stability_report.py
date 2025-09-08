#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
stability_report.py

Собирает диагностику и формирует:
- artifacts/summary/stability.tsv
- artifacts/summary/ab_diff.csv     (пишется только при различиях)
- artifacts/summary/ab_report.md    (с явной строкой RESULT: OK|FAIL)

Ожидаемая структура входа:
artifacts/
  reports/
    <test>_r<rev>/
      meta.json
      response.txt
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple

ART_ROOT = Path("artifacts")
REPORTS_DIR = ART_ROOT / "reports"
SUMMARY_DIR = ART_ROOT / "summary"
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def _sha12_from_text(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", "ignore")).hexdigest()[:12]


def _read_text_safely(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _parse_rev(dir_name: str) -> Optional[int]:
    # ожидаем шаблон вида "..._r<rev>"
    if "_r" not in dir_name:
        return None
    try:
        return int(dir_name.rsplit("_r", 1)[-1])
    except ValueError:
        return None


def _save_ab_diff(rows: List[Dict[str, str]], path: Path = SUMMARY_DIR / "ab_diff.csv") -> None:
    """Безопасно сохранить diff; если пусто — ничего не писать."""
    if not rows:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "test",
            "rev_prev",
            "rev_curr",
            "hash_prev",
            "hash_curr",
            "len_prev",
            "len_curr",
        ]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
    except Exception:
        # отчёт не должен падать из-за сохранения diff
        pass


def collect_targets() -> List[str]:
    """Собираем уникальные имена тестов по папкам '<test>_r*/meta.json'."""
    if not REPORTS_DIR.exists():
        return []
    tests = set()
    for meta in REPORTS_DIR.glob("*_r*/meta.json"):
        tests.add(meta.parent.name.split("_r", 1)[0])
    return sorted(tests)


def build_stability() -> Path:
    """
    Строим сводную таблицу:
    test, runs, min_len, max_len, unique_hashes
    """
    out = SUMMARY_DIR / "stability.tsv"
    tests = collect_targets()

    rows: List[Tuple[str, int, int, int, int]] = []
    for t in tests:
        metas = sorted(
            REPORTS_DIR.glob(f"{t}_r*/meta.json"),
            key=lambda p: (_parse_rev(p.parent.name) or -1),
        )
        if not metas:
            continue

        lengths: List[int] = []
        hashes: List[str] = []
        for m in metas:
            text = _read_text_safely(m.parent / "response.txt")
            lengths.append(len(text))
            hashes.append(_sha12_from_text(text))

        runs = len(metas)
        mn = min(lengths)
        mx = max(lengths)
        uniq = len(set(hashes))
        rows.append((t, runs, mn, mx, uniq))

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        f.write("test\truns\tmin_len\tmax_len\tunique_hashes\n")
        for t, r, mn, mx, uq in rows:
            f.write(f"{t}\t{r}\t{mn}\t{mx}\t{uq}\n")

    print(f"OK -> {out}")
    return out


def build_ab_diff() -> List[Dict[str, str]]:
    """
    Сравниваем две последние ревизии по каждому тесту.
    Если хэши ответов различаются — добавляем строку в diff.
    """
    tests = collect_targets()
    diffs: List[Dict[str, str]] = []

    for t in tests:
        runs = sorted(
            (p.parent for p in REPORTS_DIR.glob(f"{t}_r*/meta.json")),
            key=lambda d: (_parse_rev(d.name) or -1),
        )
        if len(runs) < 2:
            continue

        a, b = runs[-2], runs[-1]
        rev_a = str(_parse_rev(a.name) or "")
        rev_b = str(_parse_rev(b.name) or "")

        txt_a = _read_text_safely(a / "response.txt")
        txt_b = _read_text_safely(b / "response.txt")
        h_a = _sha12_from_text(txt_a)
        h_b = _sha12_from_text(txt_b)

        if h_a != h_b:
            diffs.append(
                {
                    "test": t,
                    "rev_prev": rev_a,
                    "rev_curr": rev_b,
                    "hash_prev": h_a,
                    "hash_curr": h_b,
                    "len_prev": str(len(txt_a)),
                    "len_curr": str(len(txt_b)),
                }
            )

    _save_ab_diff(diffs)
    return diffs


def write_ab_report_md(diffs: List[Dict[str, str]]) -> Path:
    """Пишем сводку и RESULT-строку."""
    md = SUMMARY_DIR / "ab_report.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    fail = bool(diffs)
    result = "FAIL" if fail else "OK"

    lines = ["# A/B report\n", f"\nRESULT: {result}\n"]
    if fail:
        lines.append("\n## Differences\n\n")
        lines.append(
            "| test | rev_prev | rev_curr | hash_prev | hash_curr | len_prev | len_curr |\n"
        )
        lines.append(
            "|------|----------|----------|-----------|-----------|----------|----------|\n"
        )
        for d in diffs:
            lines.append(
                f"| {d['test']} | {d['rev_prev']} | {d['rev_curr']} | "
                f"{d['hash_prev']} | {d['hash_curr']} | {d['len_prev']} | {d['len_curr']} |\n"
            )

    md.write_text("".join(lines), encoding="utf-8")
    print(f"OK -> {md}")
    return md


def main() -> int:
    build_stability()
    diffs = build_ab_diff()
    write_ab_report_md(diffs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
