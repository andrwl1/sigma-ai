import pandas as pd
import matplotlib.pyplot as plt
import os

summary_dir = "artifacts/summary"
os.makedirs(summary_dir, exist_ok=True)

# Заглушка: простой график
plt.figure()
plt.title("Pass-rate trend (placeholder)")
plt.plot([0, 1], [0, 1])
plt.savefig(os.path.join(summary_dir, "passrate.png"))
print("Saved placeholder trend plot to", summary_dir)
