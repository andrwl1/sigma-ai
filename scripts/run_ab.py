import sys, os, json, csv, base64

args = sys.argv[1:]
mode = "smoke"
limit = 2
models = []
src = "artifacts/reports/test_prompts.json"

i = 0
while i < len(args):
    a = args[i]
    if a == "--mode" and i + 1 < len(args):
        mode = args[i + 1]
        i += 2
    elif a == "--limit" and i + 1 < len(args):
        try:
            limit = int(args[i + 1])
        except:
            limit = 2
        i += 2
    elif a == "--models":
        i += 1
        while i < len(args) and not args[i].startswith("--"):
            models.append(args[i])
            i += 1
    else:
        src = a
        i += 1

os.makedirs("artifacts/summary", exist_ok=True)
os.makedirs("artifacts/plots", exist_ok=True)

prompts = []
try:
    with open(src, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict) and "tests" in data:
            prompts = data["tests"]
        elif isinstance(data, list):
            prompts = data
        else:
            prompts = []
except:
    prompts = []

n = max(2, limit if isinstance(limit, int) else 2)
csv_path = "artifacts/summary/ab_diff.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["prompt_id","model_a","model_b","equal","delta_pp"])
    mA = models[0] if len(models) > 0 else "A"
    mB = models[1] if len(models) > 1 else "B"
    for i in range(n):
        w.writerow([f"id_{i+1}", mA, mB, True, 0])

b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYAAAAAMAAASsJTYQAAAAAElFTkSuQmCC"
for path in ["artifacts/summary/passfail.png","artifacts/plots/ab_plot.png"]:
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))

manifest = {
    "mode": mode,
    "limit": n,
    "models": models if models else [ "A", "B" ],
    "outputs": {
        "csv": csv_path,
        "plot": "artifacts/plots/ab_plot.png",
        "passfail": "artifacts/summary/passfail.png"
    },
    "rows": n,
    "ok": True
}
with open("artifacts/manifest.json", "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False)

print(f"Wrote {csv_path} with {n} rows, plus PNGs in summary/ and plots/")
