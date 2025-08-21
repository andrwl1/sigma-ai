# src/log_event.py
import csv
from datetime import datetime
from pathlib import Path
import argparse

# Пути и схема
LOG_FILE = Path("outputs/data/subjectivity_log.csv")
FIELDS   = ["Day", "Environment", "Manifestation", "Axis", "Timestamp"]
ALLOWED_AXES = {"субъектность", "воля", "логика", "этика", "границы", "рефлексия"}

def ensure_csv():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()

def append_row(day: str, env: str, manif: str, axis: str):
    axis_norm = axis.strip().lower()
    if axis_norm not in ALLOWED_AXES:
        raise ValueError(
            f"Недопустимая ось: '{axis}'. Разрешены: {', '.join(sorted(ALLOWED_AXES))}"
        )
    row = {
        "Day": day.strip(),
        "Environment": env.strip(),
        "Manifestation": manif.strip(),
        "Axis": axis_norm,
        "Timestamp": datetime.now().isoformat(),  # совместимо с текущими скриптами
    }
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(row)
    print("✅ Запись добавлена:", row)

def main():
    p = argparse.ArgumentParser(description="Логирование события + автоотчёты")
    p.add_argument("--day",  required=True, help="например: 'Day 3' или '2025-08-19'")
    p.add_argument("--env",  required=True, help="контекст/что сделано")
    p.add_argument("--axis", required=True, help="ось: субъектность/воля/логика/этика/границы/рефлексия")
    p.add_argument("--manif", default="Мишель", help="кто/что проявилось (по умолчанию: Мишель)")
    args = p.parse_args()

    ensure_csv()
    append_row(args.day, args.env, args.manif, args.axis)

    # автографики и статус
    try:
        from src.log_manager import build_plots
        build_plots()
    except Exception as e:
        print("plots skipped:", e)

    try:
        from src.report import generate_status
        print("\nSTATUS:\n" + generate_status(save=True))
    except Exception as e:
        print("report skipped:", e)

if __name__ == "__main__":
    main()

