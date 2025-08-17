import sys
import platform
import json
import requests

def probe():
    r = requests.get("https://httpbin.org/get", timeout=10)
    r.raise_for_status()
    data = r.json()
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "ok": r.ok,
        "url": data.get("url"),
    }

if __name__ == "__main__":
    print(json.dumps(probe(), ensure_ascii=False, indent=2))
