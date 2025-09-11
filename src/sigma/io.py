import requests


def fetch_json(url: str, timeout: int = 10) -> dict:
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    print(fetch_json("https://httpbin.org/json"))
