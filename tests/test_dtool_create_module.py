"""Test the dtool_create module."""


def test_version_is_string():
    import dtool_create
    assert isinstance(dtool_create.__version__, str)
