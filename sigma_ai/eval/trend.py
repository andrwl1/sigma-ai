import pathlib, matplotlib.pyplot as plt, pandas as pd

def plot_trend(csv_path, png_path):
    df = pd.read_csv(csv_path)
    if "timestamp" not in df or "accuracy" not in df:
        pathlib.Path(png_path).write_bytes(b"")
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    plt.figure(figsize=(8,4))
    plt.plot(df["timestamp"], df["accuracy"], marker="o")
    plt.title("Accuracy trend")
    plt.xlabel("Time")
    plt.ylabel("Accuracy")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(png_path)
