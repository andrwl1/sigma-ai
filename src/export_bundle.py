from pathlib import Path
import zipfile, time

reports = Path("reports")
bundle_dir = Path("bundle"); bundle_dir.mkdir(exist_ok=True)
stamp = time.strftime("%Y%m%d_%H%M%S")
zip_path = bundle_dir / f"bundle_{stamp}.zip"

with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
    if reports.exists():
        for p in reports.rglob("*"):
            if p.is_file():
                z.write(p, p.as_posix())
print(f"export_bundle: saved -> {zip_path}")
