from typing import Sequence

def non_empty(text: str) -> None:
    assert isinstance(text, str), "value is not a string"
    assert text.strip(), "text is empty or whitespace"

def max_len(text: str, limit: int = 2048) -> None:
    assert len(text) <= limit, f"text too long: {len(text)} > {limit}"

def no_tabs(text: str) -> None:
    assert "\t" not in text, "tabs are not allowed (use \\t only in TSV files, not in content)"

def all_checks(text: str, limit: int = 2048, extra: Sequence[str] | None = None) -> None:
    non_empty(text); max_len(text, limit); no_tabs(text)
    if extra:
        for token in extra:
            assert token not in text, f"forbidden token: {token!r}"
