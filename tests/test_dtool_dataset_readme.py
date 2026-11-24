"""Test the ``dtool readme`` write, validate, edit and interactive commands."""

import click
import pytest
from click.testing import CliRunner

from dtoolcore import DataSet, ProtoDataSet

VALID_YAML = "description: integration test\nproject: dtool\n"
FORMATTED_YAML = "---\ndescription: integration test\nproject: dtool\n"
INVALID_YAML = "description: [unclosed\n"


@pytest.fixture(autouse=True)
def isolated_config(tmp_path, monkeypatch):
    """Ignore the user's dtool config file and DTOOL_* environment."""
    import dtool_create.dataset

    monkeypatch.setattr(dtool_create.dataset, "CONFIG_PATH",
                        str(tmp_path / "dtool.json"))
    for key in ("DTOOL_README_TEMPLATE_FPATH", "DTOOL_USER_EMAIL",
                "DTOOL_USER_FULL_NAME"):
        monkeypatch.delenv(key, raising=False)


def invoke(command, *args, input=None):
    return CliRunner().invoke(command, [str(a) for a in args], input=input)


def run(command, *args, input=None):
    result = invoke(command, *args, input=input)
    assert result.exit_code == 0, result.output
    return result.output


@pytest.fixture
def proto_uri(tmp_path):
    from dtool_create.dataset import create

    return run(create, "-q", "readme_test", tmp_path).strip()


@pytest.fixture
def frozen_uri(proto_uri):
    from dtool_create.dataset import freeze

    run(freeze, proto_uri)
    return proto_uri


def readme_of(uri):
    try:
        return ProtoDataSet.from_uri(uri).get_readme_content()
    except Exception:
        return DataSet.from_uri(uri).get_readme_content()


# --- dtool readme write ------------------------------------------------------

def test_write_from_file(proto_uri, tmp_path):
    from dtool_create.dataset import write

    readme = tmp_path / "readme.yml"
    readme.write_text(VALID_YAML)
    run(write, proto_uri, readme)
    assert readme_of(proto_uri) == FORMATTED_YAML


def test_write_from_stdin(proto_uri):
    from dtool_create.dataset import write

    run(write, proto_uri, "-", input=VALID_YAML)
    assert readme_of(proto_uri) == FORMATTED_YAML


def test_write_to_frozen_dataset(frozen_uri):
    from dtool_create.dataset import write

    run(write, frozen_uri, "-", input=VALID_YAML)
    assert readme_of(frozen_uri) == FORMATTED_YAML


def test_write_invalid_yaml(proto_uri):
    from dtool_create.dataset import write

    before = readme_of(proto_uri)
    result = invoke(write, proto_uri, "-", input=INVALID_YAML)
    assert result.exit_code == 5
    assert "Invalid YAML" in result.output
    assert "Did not update readme" in result.output
    assert readme_of(proto_uri) == before


# --- dtool readme validate ---------------------------------------------------

@pytest.mark.parametrize("dataset", ["proto_uri", "frozen_uri"])
def test_validate(dataset, request):
    from dtool_create.dataset import validate

    uri = request.getfixturevalue(dataset)
    assert "All good!" in run(validate, uri)


def test_validate_invalid_yaml(proto_uri):
    from dtool_create.dataset import validate

    ProtoDataSet.from_uri(proto_uri).put_readme(INVALID_YAML)
    output = run(validate, proto_uri)
    assert "Invalid YAML" in output
    assert "All good!" not in output


# --- dtool readme edit -------------------------------------------------------

@pytest.mark.parametrize("dataset", ["proto_uri", "frozen_uri"])
def test_edit(dataset, request, monkeypatch):
    from dtool_create.dataset import edit

    uri = request.getfixturevalue(dataset)
    seen = {}

    def fake_edit(text, extension):
        seen["text"], seen["extension"] = text, extension
        return VALID_YAML

    monkeypatch.setattr(click, "edit", fake_edit)
    output = run(edit, uri)
    assert "Updated readme" in output
    assert seen == {"text": "", "extension": ".yml"}
    assert readme_of(uri) == FORMATTED_YAML


def test_edit_without_changes(proto_uri, monkeypatch):
    from dtool_create.dataset import edit

    ProtoDataSet.from_uri(proto_uri).put_readme(VALID_YAML)
    monkeypatch.setattr(click, "edit", lambda text, extension: None)
    assert "Did not update readme" in run(edit, proto_uri)
    assert readme_of(proto_uri) == VALID_YAML


# --- dtool readme interactive ------------------------------------------------

def test_interactive_with_default_template(proto_uri, monkeypatch):
    from dtool_create.dataset import interactive

    monkeypatch.setenv("DTOOL_USER_FULL_NAME", "Postman Pat")
    monkeypatch.setenv("DTOOL_USER_EMAIL", "pat@example.com")
    answers = [
        "My dataset",   # description
        "",             # project: keep default
        "",             # confidential: keep default
        "",             # personally_identifiable_information
        "",             # owners/name: keep default
        "",             # owners/email: keep default
        "",             # owners/username: keep default
    ]
    output = run(interactive, proto_uri, input="\n".join(answers) + "\n")
    assert "Updated readme" in output

    readme = readme_of(proto_uri)
    assert "description: My dataset" in readme
    assert "project: Project name" in readme
    assert "confidential: false" in readme
    assert "name: Postman Pat" in readme
    assert "email: pat@example.com" in readme


def test_interactive_with_custom_template(proto_uri, tmp_path, monkeypatch):
    from dtool_create.dataset import interactive

    template = tmp_path / "template.yml"
    template.write_text(
        "---\nsample: S1\nconcentration: 1.5\nmeasured: 2024-01-01\n"
        "funding:\n  agency: Agency A\n")
    monkeypatch.setenv("DTOOL_README_TEMPLATE_FPATH", str(template))
    answers = [
        "S2",           # sample
        "2.5",          # concentration (a float)
        "not-a-date",   # measured: rejected ...
        "2024-02-03",   # ... then accepted
        "Agency B",     # funding/agency (a nested mapping)
    ]
    output = run(interactive, proto_uri, input="\n".join(answers) + "\n")
    assert "Could not parse date" in output

    assert readme_of(proto_uri) == (
        "---\nsample: S2\nconcentration: 2.5\nmeasured: 2024-02-03\n"
        "funding:\n  agency: Agency B\n")


def test_interactive_keeps_default_date(proto_uri, tmp_path, monkeypatch):
    from dtool_create.dataset import interactive

    template = tmp_path / "template.yml"
    template.write_text("---\nmeasured: 2024-01-01\n")
    monkeypatch.setenv("DTOOL_README_TEMPLATE_FPATH", str(template))

    run(interactive, proto_uri, input="\n")
    assert readme_of(proto_uri) == "---\nmeasured: 2024-01-01\n"
