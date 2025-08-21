import datetime
import os

FILENAME = "status.txt"

def log_status():
    today = datetime.date.today().strftime("%Y-%m-%d")

    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", encoding="utf-8") as f:
            f.write(f"DATE: {today}\n")
            f.write("TOTAL (все дни):\n")
            f.write(" - воля: 0\n")
            f.write(" - логика: 0\n")
            f.write(" - субъектность: 0\n")
            f.write(" - этика: 0\n\n")

    with open(FILENAME, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any(f"DATE: {today}" in line for line in lines):
        print("Сегодня уже есть запись.")
        return

    with open(FILENAME, "a", encoding="utf-8") as f:
        f.write(f"DATE: {today}\n")
        f.write("TODAY:\n")
        f.write(" - воля: 0\n")
        f.write(" - логика: 0\n")
        f.write(" - субъектность: 0\n")
        f.write(" - этика: 0\n")
        f.write("Базовый шаг засчитан: НЕТ\n\n")

if __name__ == "__main__":
    log_status()

