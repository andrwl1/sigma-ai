import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

log_file = Path("logs/sample.csv")
out_file = Path("reports/plots/loss.png")
out_file.parent.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(log_file)
plt.figure()
df.plot(x="epoch", y="loss", title="Loss curve")
plt.savefig(out_file)

print(f"plot_logs: saved -> {out_file}")
