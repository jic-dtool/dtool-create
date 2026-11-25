"""Test error paths and less common options of the dataset commands."""

import os

import pytest
from click.testing import CliRunner

from dtoolcore import DataSet, ProtoDataSet


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Ignore the user's dtool config file and DTOOL_* environment."""
    import dtool_create.dataset

    monkeypatch.setattr(dtool_create.dataset, "CONFIG_PATH",
                        str(tmp_path / "dtool.json"))
    monkeypatch.delenv("DTOOL_MAX_FILES_LIMIT", raising=False)


def invoke(command, *args, input=None):
    return CliRunner().invoke(command, [str(a) for a in args], input=input)


def run(command, *args):
    result = invoke(command, *args)
    assert result.exit_code == 0, result.output
    return result.output


@pytest.fixture
def datasets_dir(tmp_path):
    path = tmp_path / "datasets"
    path.mkdir()
    return path


def make_proto(base, name="errors_test", items=("a.txt", "b.txt")):
    """Create a proto dataset with ``items``; return its URI."""
    from dtool_create.dataset import add, create

    uri = run(create, "-q", name, base).strip()
    data = base.parent / "data"
    data.mkdir(exist_ok=True)
    for relpath in items:
        fpath = data / "item"
        fpath.write_text(relpath)
        run(add, "item", fpath, uri, relpath)
    return uri


@pytest.fixture
def frozen_uri(datasets_dir):
    from dtool_create.dataset import freeze

    uri = make_proto(datasets_dir)
    run(freeze, uri)
    return uri


# --- create ------------------------------------------------------------------

def test_create_invalid_name(datasets_dir):
    from dtool_create.dataset import create

    result = invoke(create, "not a valid name!", datasets_dir)
    assert result.exit_code == 6
    assert "Invalid dataset name" in result.output
    assert os.listdir(datasets_dir) == []


def test_create_symlink_requires_symlink_path(datasets_dir):
    from dtool_create.dataset import create

    result = invoke(create, "linked", "symlink:" + str(datasets_dir))
    assert result.exit_code == 2
    assert "--symlink-path" in result.output


def test_create_symlink_dataset(datasets_dir, tmp_path):
    from dtool_create.dataset import create, freeze

    data = tmp_path / "linked-data"
    data.mkdir()
    (data / "file.txt").write_text("hello")

    uri = run(create, "-q", "linked", datasets_dir, "-s", data).strip()
    assert uri.startswith("symlink:")
    run(freeze, uri)
    dataset = DataSet.from_uri(uri)
    assert [dataset.item_properties(i)["relpath"]
            for i in dataset.identifiers] == ["file.txt"]


# --- add metadata ------------------------------------------------------------

def test_add_metadata(datasets_dir):
    from dtool_create.dataset import add, freeze

    uri = make_proto(datasets_dir)
    run(add, "metadata", uri, "a.txt", "kind", "text")
    run(freeze, uri)

    dataset = DataSet.from_uri(uri)
    by_relpath = {dataset.item_properties(i)["relpath"]: value
                  for i, value in dataset.get_overlay("kind").items()}
    assert by_relpath["a.txt"] == "text"


# --- freeze ------------------------------------------------------------------

def test_freeze_too_many_items(datasets_dir, monkeypatch):
    from dtool_create.dataset import freeze

    uri = make_proto(datasets_dir)
    monkeypatch.setenv("DTOOL_MAX_FILES_LIMIT", "1")
    result = invoke(freeze, uri)
    assert result.exit_code == 2
    assert "Too many items (2 > 1)" in result.output
    # Still a proto dataset.
    ProtoDataSet.from_uri(uri)


def test_freeze_invalid_item_name(datasets_dir):
    from dtool_create.dataset import freeze

    uri = make_proto(datasets_dir, items=("bad\nname.txt",))
    result = invoke(freeze, uri)
    assert result.exit_code == 3
    assert "Invalid item name" in result.output
    ProtoDataSet.from_uri(uri)


# --- copy / cp ---------------------------------------------------------------

def test_copy_is_deprecated_but_works(frozen_uri, tmp_path):
    from dtool_create.dataset import copy

    dest = tmp_path / "copies"
    dest.mkdir()
    result = invoke(copy, "-q", frozen_uri, dest)
    assert result.exit_code == 0, result.output
    assert "deprecated" in result.output
    copied = result.output.strip().splitlines()[-1]
    assert DataSet.from_uri(copied).uuid == DataSet.from_uri(frozen_uri).uuid


def test_cp_refuses_existing_path(frozen_uri, tmp_path):
    from dtool_create.dataset import cp

    dest = tmp_path / "copies"
    (dest / "errors_test").mkdir(parents=True)
    result = invoke(cp, frozen_uri, dest)
    assert result.exit_code == 2
    assert "Path already exists" in result.output


def test_cp_resume(frozen_uri, tmp_path):
    import dtoolcore
    from dtool_create.dataset import cp

    dest = tmp_path / "copies"
    dest.mkdir()
    source = DataSet.from_uri(frozen_uri)
    # Simulate an interrupted copy: dtoolcore.copy first creates the
    # destination proto dataset, then copies the items and freezes it.
    dtoolcore._copy_create_proto_dataset(source, str(dest), None, None)

    copied = run(cp, "--resume", "-q", frozen_uri, dest).strip()
    copy = DataSet.from_uri(copied)
    assert copy.uuid == source.uuid
    assert sorted(copy.identifiers) == sorted(source.identifiers)


# --- publish -----------------------------------------------------------------

@pytest.mark.parametrize("quiet", [False, True])
def test_publish(frozen_uri, monkeypatch, quiet):
    import dtool_create.publish

    url = "https://example.com/dataset"
    calls = []
    monkeypatch.setattr(dtool_create.publish, "http_publish",
                        lambda uri: calls.append(uri) or url)

    args = ["-q", frozen_uri] if quiet else [frozen_uri]
    output = run(dtool_create.publish.publish, *args)
    assert calls == [frozen_uri]
    if quiet:
        assert output.strip() == url
    else:
        assert output.strip() == "Dataset accessible at " + url
