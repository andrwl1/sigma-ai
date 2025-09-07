import pytest
from src.validators import all_checks, non_empty, max_len, no_tabs

@pytest.mark.t300
def test_non_empty_ok():
    non_empty("hello")

@pytest.mark.t300
def test_non_empty_rejects_whitespace():
    with pytest.raises(AssertionError):
        non_empty("   ")

@pytest.mark.t300
def test_non_empty_rejects_empty():
    with pytest.raises(AssertionError):
        non_empty("")

@pytest.mark.t300
def test_max_len_border_ok():
    s = "a" * 2048
    max_len(s, 2048)

@pytest.mark.t300
def test_max_len_violation():
    with pytest.raises(AssertionError):
        max_len("x" * 2049, 2048)

@pytest.mark.t300
@pytest.mark.parametrize("bad", ["contains\ttab", "foo\tbar"])
def test_no_tabs(bad):
    with pytest.raises(AssertionError):
        no_tabs(bad)

@pytest.mark.t300
@pytest.mark.parametrize(
    "text,limit,extras",
    [
        ("OK text", 100, None),
        ("Edge", 4, None),
    ],
)
def test_all_checks_pass(text, limit, extras):
    all_checks(text, limit, extras)

@pytest.mark.t300
def test_all_checks_forbidden_token():
    with pytest.raises(AssertionError):
        all_checks("secret key here", 100, extra=["secret"])

@pytest.mark.t300
@pytest.mark.parametrize("bad", ["DROP TABLE users", "-- comment", "пароль=123", "秘密"])
def test_all_checks_realistic_forbidden(bad):
    with pytest.raises(AssertionError):
        all_checks(bad, 100, extra=["DROP", "--", "пароль", "秘密"])
