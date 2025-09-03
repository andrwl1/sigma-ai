import pathlib, glob, hashlib, json, re
root = pathlib.Path("artifacts/reports")
targets = sorted({p.parent.name.split("_r")[0] for p in root.glob("T*/meta.json")})
rows = []
for t in targets:
    metas = sorted(root.glob(f"{t}_r*/meta.json"))
    if not metas: 
        continue
    lens, hashes = [], []
    for m in metas:
        res = (m.parent/"response.txt").read_text(encoding="utf-8", errors="ignore")
        lens.append(len(res))
        hashes.append(hashlib.sha1(res.encode("utf-8", errors="ignore")).hexdigest()[:12])
    uniq = len(set(hashes))
    rows.append((t, len(metas), min(lens), max(lens), uniq))
out = pathlib.Path("artifacts/summary/stability.tsv")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("test\truns\tmin_len\tmax_len\tunique_hashes\n" + 
               "\n".join(f"{t}\t{n}\t{mn}\t{mx}\t{u}" for t,n,mn,mx,u in rows),
               encoding="utf-8")
print(f"OK -> {out}")
