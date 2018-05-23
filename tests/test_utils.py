"""Test the utility functions."""


def test_valid_handle():
    from dtool_create.utils import valid_handle
    assert valid_handle("this/is/a/normal/relpath")
    assert not valid_handle("this has a \n newline")
