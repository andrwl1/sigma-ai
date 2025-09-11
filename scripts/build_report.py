import os


def build_report(artifacts_dir, output_file):
    md = []
    md.append("| Test | Model | Timestamp | Req Short | First Short |")
    md.append("|------|-------|-----------|-----------|-------------|")

    for root, dirs, files in os.walk(artifacts_dir):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    lines = f.readlines()
                    t = file.replace(".txt", "")
                    model = "unknown"
                    ts = "unknown"
                    req_short = lines[0].strip() if len(lines) > 0 else ""
                    first_short = lines[1].strip() if len(lines) > 1 else ""

                    # безопасное экранирование пайпов
                    req_safe = req_short.replace("|", "\\|")
                    first_safe = first_short.replace("|", "\\|")

                    md.append(f"| {t} | {model} | {ts} | {req_safe} | {first_safe} |")

    with open(output_file, "w") as out:
        out.write("\n".join(md))


if __name__ == "__main__":
    build_report("artifacts", "artifacts/summary/preci_report.md")
