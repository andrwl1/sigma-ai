#!/usr/bin/env python3
import argparse
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Append RESULT line to ab_report.md")
    parser.add_argument(
        "--delta", type=float, required=True, help="Отклонение в п.п. (например, 0.75 или -1.2)"
    )
    parser.add_argument(
        "--threshold", type=int, default=None, help="Порог в п.п. (перекрывает THRESHOLD_PP)"
    )
    args = parser.parse_args()

    threshold_pp = (
        args.threshold if args.threshold is not None else int(os.getenv("THRESHOLD_PP", 2))
    )
    delta_pp = round(args.delta, 2)

    result = "OK" if abs(delta_pp) <= threshold_pp else "FAIL"

    out = Path("ab_report.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_text("# AB report\n\n", encoding="utf-8")

    with out.open("a", encoding="utf-8") as f:
        f.write(f"\nRESULT={result}; Δ={delta_pp}pp; threshold={threshold_pp}pp\n")

    print(f"RESULT={result}; Δ={delta_pp}pp; threshold={threshold_pp}pp")


if __name__ == "__main__":
    main()
