# tests/test_imports.py
import importlib
import pkgutil
import sys
import pytest

import analyzer

def test_all_analyzer_modules_importable():
    """
    Dynamically find all modules and sub‑packages under `analyzer` and attempt to import them.
    Fails the test if any module raises an exception on import.
    """
    base_pkg = analyzer
    base_name = base_pkg.__name__
    path = getattr(base_pkg, "__path__", None)
    assert path is not None, f"{base_name} is not a package with __path__"

    failed = {}

    for finder, mod_name, is_pkg in pkgutil.walk_packages(path, prefix=base_name + "."):
        try:
            importlib.invalidate_caches()
            importlib.import_module(mod_name)
        except Exception as e:
            failed[mod_name] = repr(e)

    if failed:
        msgs = "\n".join(f"- {name}: {err}" for name, err in failed.items())
        pytest.fail(f"The following modules under {base_name} failed to import:\n{msgs}")
