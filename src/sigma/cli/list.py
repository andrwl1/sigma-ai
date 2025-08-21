import os
import json
from collections import Counter
from sigma.core.models import Axis

EVIDENCE_DIR = "evidence"

def run():
    counts = Counter()
    for axis in Axis:
        path = os.path.join(EVIDENCE_DIR, axis.value, "logs", "events.jsonl")
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    try:
                        json.loads(line)
                        counts[axis.value] += 1
                    except:
                        continue
    print("📊 Evidence summary:")
    for axis in Axis:
        print(f"{axis.value:20} {counts[axis.value]}")
