import csv
from datetime import datetime
from pathlib import Path
import os

# ----- Константы -----
LOG_FILE = Path("outputs/data/subjectivity_log.csv")
PLOTS_DIR = Path("outputs/plots")
ALLOWED_AXES = {"субъектность", "воля", "логика", "этика", "границы", "рефлексия"}

# ----- Логирование -----
def add_log_entry(day: str, environment: str, manifestation: str, axis: str):
    axis_norm = axis.strip().lower()
    if axis_norm not in ALLOWED_AXES:
        raise ValueError(
            f"Недопустимая ось: '{axis}'. Разрешены: {', '.join(sorted(ALLOWED_AXES))}"
        )

    entry = {
        "Day": day.strip(),
        "Environment": environment.strip(),
        "Manifestation": manifestation.strip(),
        "Axis": axis_norm,
        "Timestamp": datetime.now().isoformat()
    }

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=entry.keys())
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(entry)

    print("Запись добавлена:", entry)

# ----- Построение графиков -----
def build_plots():
    import pandas as pd
    import matplotlib.pyplot as plt

    if not LOG_FILE.exists():
        print("Лога ещё нет, графики пропущены.")
        return

    df = pd.read_csv(LOG_FILE)
    if "Timestamp" in df.columns:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Кол-во записей по осям
    plt.figure()
    df["Axis"].value_counts().sort_index().plot(kind="bar")
    plt.title("Количество записей по осям")
    plt.xlabel("Ось")
    plt.ylabel("Кол-во записей")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "axis_counts.png")
    plt.close()

    # 2) Кол-во записей по дням
    plt.figure()
    df["Day"].value_counts().sort_index().plot(kind="bar")
    plt.title("Количество записей по дням")
    plt.xlabel("Day")
    plt.ylabel("Кол-во записей")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "day_counts.png")
    plt.close()

    # 3) Stacked: оси по дням
    pivot = (
        df.pivot_table(index="Day", columns="Axis", values="Timestamp", aggfunc="count")
          .fillna(0)
          .sort_index()
    )
    plt.figure()
    pivot.plot(kind="bar", stacked=True)
    plt.title("Записи по осям и дням (stacked)")
    plt.xlabel("Day")
    plt.ylabel("Кол-во записей")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "axis_by_day.png")
    plt.close()

    print("Графики обновлены:",
          PLOTS_DIR / "axis_counts.png",
          PLOTS_DIR / "day_counts.png",
          PLOTS_DIR / "axis_by_day.png", sep="\n - ")

# ----- CLI -----
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Log entry + auto-plots + status")
    parser.add_argument("--day", required=True, help="Напр., 'Day 3'")
    parser.add_argument("--env", required=True, help="Кратко: что сделал")
    parser.add_argument("--axis", required=True,
                        help="Ось: субъектность/воля/логика/этика/границы/рефлексия")
    parser.add_argument("--manif", default="Мишель", help="Кто/что проявилось")
    args = parser.parse_args()

    add_log_entry(args.day, args.env, args.manif, args.axis)
    build_plots()

    # Генерация текстового статуса
    try:
        from src.report import generate_status
        status_txt = generate_status(save=True)
        print("\nSTATUS:\n" + status_txt)
    except Exception as e:
        print("report skipped:", e)

