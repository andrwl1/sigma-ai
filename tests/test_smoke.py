def test_runtime():
    import sys, importlib
    assert sys.version_info >= (3, 10)
    for m in ["requests","pandas","numpy","matplotlib"]:
        importlib.import_module(m)
