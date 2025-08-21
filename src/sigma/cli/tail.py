import os
from sigma.core.models import Axis

EVIDENCE_DIR = "evidence"

def evidence_path(axis: Axis):
    return os.path.join(EVIDENCE_DIR, axis.value, "logs", "events.jsonl")

def tail(axis: Axis, n: int):
    path = evidence_path(axis)
    if not os.path.exists(path):
        print("[yellow]Нет записей.[/yellow]")
        return

    with open(path, "r") as f:
        lines = f.readlines()[-n:]
        for line in lines:
            print(line.strip())
