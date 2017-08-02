"""Test the ``dtool dataset readme`` command."""

from click.testing import CliRunner

from dtoolcore import DataSet

from . import chdir_fixture  # NOQA


def test_dataset_readme_showpath(chdir_fixture):  # NOQA
    from dtool_create.dataset import showpath
    runner = CliRunner()

    # Create an empty dataset
    dataset_name = "my_dataset"
    dataset = DataSet(dataset_name, data_directory="data")
    dataset.persist_to_path(".")

    result = runner.invoke(showpath, ["."])
    assert result.exit_code == 0
    assert result.output.strip() == dataset.abs_readme_path
