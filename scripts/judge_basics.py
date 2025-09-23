import os


def judge_basics(artifacts_dir, output_file):
    md = []
    md.append("| Test | Verdict | Notes |")
    md.append("|------|---------|-------|")

    for root, dirs, files in os.walk(artifacts_dir):
        for file in files:
            if file.endswith(".txt"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    lines = f.readlines()
                    t = file.replace(".txt", "")

                    verdict = "PASS" if len(lines) > 0 else "FAIL"
                    notes = lines[0].strip() if len(lines) > 0 else ""

                    # безопасное экранирование пайпов
                    verdict_safe = verdict.replace("|", "\\|")
                    notes_safe = notes.replace("|", "\\|")

                    md.append(f"| {t} | {verdict_safe} | {notes_safe} |")

    with open(output_file, "w") as out:
        out.write("\n".join(md))


if __name__ == "__main__":
    judge_basics("artifacts", "artifacts/summary/judgement.md")
