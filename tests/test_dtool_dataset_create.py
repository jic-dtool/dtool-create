"""Test the ``dtool dataset create`` command."""

import os

from click.testing import CliRunner

from dtoolcore import DataSet

from . import chdir_fixture, tmp_dir_fixture  # NOQA


def test_dataset_create_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    # Test that the dataset has been created.
    dataset = DataSet.from_path(dataset_name)

    # Test that the dataset name is correct.
    assert dataset.name == dataset_name



def test_dataset_create_fails_on_directory_exists(chdir_fixture):  # NOQA
    from dtool_create.dataset import create
    runner = CliRunner()

    dataset_name = "my_dataset"
    os.mkdir(dataset_name)
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code != 0
    assert result.output.startswith("Usage")
    assert result.output.find("File/directory already exists") != -1


def test_dataset_create_can_work_outside_current_directory(tmp_dir_fixture):  # NOQA
    from dtool_create.dataset import create
    runner = CliRunner()

    dataset_name = "my_dataset"
    dataset_path = os.path.join(tmp_dir_fixture, dataset_name)
    result = runner.invoke(create, [dataset_path])
    assert result.exit_code == 0

    # Test that the dataset has been created.
    dataset = DataSet.from_path(dataset_path)

    # Test that the dataset name is correct.
    assert dataset.name == dataset_name
