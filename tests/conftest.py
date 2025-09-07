import os, random, pytest, sys, pathlib
root = pathlib.Path(__file__).resolve().parents[1]
src = root / "src"
for p in (str(src), str(root)):
    if p not in sys.path:
        sys.path.insert(0, p)
try:
    import numpy as np
except Exception:
    np = None
@pytest.fixture(autouse=True, scope="session")
def _set_seed():
    seed = int(os.environ.get("TEST_SEED","1337"))
    random.seed(seed)
    if np is not None:
        try: np.random.seed(seed)
        except Exception: pass
    os.environ["PYTHONHASHSEED"] = str(seed)
    return seed
