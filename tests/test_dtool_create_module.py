"""Test the dtool_create module."""


def test_version_is_string():
    import dtool_create
    assert isinstance(dtool_create.__version__, str)


def test_version_when_not_installed(monkeypatch):
    import importlib
    import importlib.metadata

    import dtool_create

    def not_installed(name):
        raise importlib.metadata.PackageNotFoundError(name)

    monkeypatch.setattr(importlib.metadata, "version", not_installed)
    try:
        importlib.reload(dtool_create)
        assert dtool_create.__version__ == "unknown"
    finally:
        monkeypatch.undo()
        importlib.reload(dtool_create)
    assert dtool_create.__version__ != "unknown"
