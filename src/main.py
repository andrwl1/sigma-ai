from sigma.core import hello

if __name__ == "__main__":
    print(hello("Andrii"))


def probe():
    import platform
    return {
        "ok": True,
        "python": True,
        "platform": platform.system()
    }


