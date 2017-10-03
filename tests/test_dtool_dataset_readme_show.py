"""Test the ``dtool name`` command."""

import os

from . import chdir_fixture  # NOQA

from click.testing import CliRunner

from dtoolcore import ProtoDataSet


def test_dataset_readme_show_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create, show, freeze
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    dataset_abspath = os.path.abspath(dataset_name)
    dataset_uri = "file://{}".format(dataset_abspath)

    result = runner.invoke(show, [dataset_uri])
    assert result.exit_code == 0
    assert result.output.strip() == ""

    # Update the readme content.
    proto_dataset = ProtoDataSet.from_uri(dataset_uri)
    readme_content = "hello\nworld"
    proto_dataset.put_readme(readme_content)

    result = runner.invoke(show, [dataset_uri])
    assert result.exit_code == 0
    assert result.output.strip() == readme_content

    # Make sure that the command works on a frozen dataset.
    result = runner.invoke(freeze, [dataset_uri])
    assert result.exit_code == 0

    result = runner.invoke(show, [dataset_uri])
    assert result.exit_code == 0
    assert result.output.strip() == readme_content
