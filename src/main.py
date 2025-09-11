from sigma.core import hello
from sigma.validators import equal


def probe():
    import platform

    return {
        "ok": True,
        "python": True,
        "platform": platform.system(),
    }


def is_pass(expected, got):
    return (
        equal(expected, got, "yesno")
        or equal(expected, got, "punct")
        or equal(expected, got, "spaces")
        or equal(expected, got, "strict")
    )


if __name__ == "__main__":
    print(hello("Andrii"))
    print(is_pass("YES", "yes"))  # True
    print(is_pass("42.", "42"))  # True
    print(is_pass("a   b", "a b"))  # True
    print(is_pass("cat", "dog"))  # False
