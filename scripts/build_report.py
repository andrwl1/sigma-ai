#!/usr/bin/env python3
import re, json, statistics, os, pathlib
src = "summary/cloud_vs_local.md"
exp_path = "artifacts/reports/expected_answers.json"
out = "artifacts/reports/cloud_vs_local_report.md"

rows = []
row_re = re.compile(r'^\|\s*(?P<ts>[^|]+)\|\s*(?P<side>[^|]+)\|\s*(?P<model>[^|]+)\|\s*(?P<test>[^|]+)\|\s*(?P<elapsed>[^|]+)\|\s*(?P<answer>[^|]+)\|\s*(?P<chars>[^|]+)\|\s*(?P<words>[^|]+)\|$')

with open(src, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        m = row_re.match(line)
        if m:
            d = {k: v.strip() for k, v in m.groupdict().items()}
            # Normalize
            d["test"] = d["test"].strip()
            try:
                d["elapsed"] = float(d["elapsed"])
            except:
                d["elapsed"] = None
            rows.append(d)

with open(exp_path, 'r', encoding='utf-8') as f:
    expected = json.load(f)

# Group by test, then merge cloud/local
by_test = {}
for r in rows:
    t = r["test"]
    by_test.setdefault(t, {})
    by_test[t][r["side"]] = r

# Build per-test summary
lines = []
ok_both = 0
mismatch = 0
total_tests = 0
lat_local = []
lat_cloud = []

def norm(s):
    return re.sub(r'\s+', ' ', s.strip())

for t in sorted(by_test.keys(), key=lambda x: (x[0], int(re.sub(r'[^0-9]','', x) or 0))):
    local = by_test[t].get("local")
    cloud = by_test[t].get("cloud")
    exp = expected.get(t, "")
    la = norm(local["answer"]) if local else ""
    ca = norm(cloud["answer"]) if cloud else ""
    l_ok = (norm(exp) == la) if exp else None
    c_ok = (norm(exp) == ca) if exp else None
    same = (la == ca and la != "")
    status = "OK"
    if not (l_ok and c_ok and same):
        status = "CHECK"
        mismatch += 1
    else:
        ok_both += 1
    total_tests += 1
    if local and local["elapsed"] is not None: lat_local.append(local["elapsed"])
    if cloud and cloud["elapsed"] is not None: lat_cloud.append(cloud["elapsed"])
    lines.append(f"| {t} | {exp or ''} | {la} | {local['elapsed'] if local else ''} | {ca} | {cloud['elapsed'] if cloud else ''} | {'yes' if same else 'no'} | {status} |")

avg_loc = statistics.mean(lat_local) if lat_local else None
avg_cld = statistics.mean(lat_cloud) if lat_cloud else None

pathlib.Path(os.path.dirname(out)).mkdir(parents=True, exist_ok=True)
with open(out, 'w', encoding='utf-8') as f:
    f.write("# Cloud vs Local — Summary Report (T1–T24)\n\n")
    f.write(f"- Total tests: **{total_tests}**\n")
    f.write(f"- Both sides correct & identical: **{ok_both}**\n")
    f.write(f"- Needs check: **{mismatch}**\n")
    if avg_loc is not None and avg_cld is not None:
        faster = "local" if avg_loc < avg_cld else "cloud"
        f.write(f"- Avg latency — local: **{avg_loc:.3f}s**, cloud: **{avg_cld:.3f}s** → **{faster} faster**\n")
    f.write("\n## Per-test comparison\n")
    f.write("| Test | Expected | Local answer | Local elapsed(s) | Cloud answer | Cloud elapsed(s) | Same? | Status |\n")
    f.write("|---|---|---|---:|---|---:|---:|---|\n")
    for l in lines:
        f.write(l + "\n")
    f.write("\n_This report was auto-generated from `summary/cloud_vs_local.md`._\n")
print(f"OK -> {out}")
