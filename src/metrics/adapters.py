import os, importlib

def _load():
    spec = os.environ.get("SIGMA_MODEL_PY", "src.sigma.core:run_model")
    mod, func = spec.split(":")
    m = importlib.import_module(mod)
    return getattr(m, func)

_GEN = _load()

def generate(prompt: str) -> str:
    return _GEN(prompt)
