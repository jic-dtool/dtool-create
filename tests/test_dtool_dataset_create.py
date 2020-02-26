"""Test the ``dtool create`` command."""

import os

from click.testing import CliRunner

from dtoolcore import ProtoDataSet
from dtoolcore.utils import sanitise_uri

from . import chdir_fixture, tmp_dir_fixture  # NOQA


def test_dataset_create_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    # Test that the proto dataset has been created.
    dataset_abspath = os.path.abspath(dataset_name)
    dataset_uri = sanitise_uri(dataset_abspath)
    dataset = ProtoDataSet.from_uri(dataset_uri)

    # Test that the dataset name is correct.
    assert dataset.name == dataset_name


def test_dataset_create_quiet_flag(tmp_dir_fixture):  # NOQA
    from dtool_create.dataset import create
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [
        "--quiet",
        dataset_name,
        tmp_dir_fixture
    ])
    assert result.exit_code == 0

    dataset_path = os.path.join(tmp_dir_fixture, dataset_name)
    dataset_uri = sanitise_uri(dataset_path)
    assert result.output.strip() == dataset_uri


def test_dataset_create_fails_on_directory_exists(chdir_fixture):  # NOQA
    from dtool_create.dataset import create
    runner = CliRunner()

    dataset_name = "my_dataset"
    os.mkdir(dataset_name)
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code != 0
    assert result.output.startswith("Usage")
    assert result.output.find("already exists") != -1


def test_dataset_create_can_work_outside_current_directory(tmp_dir_fixture):  # NOQA
    from dtool_create.dataset import create
    runner = CliRunner()

    dataset_name = "my_dataset"
    dataset_path = os.path.join(tmp_dir_fixture, dataset_name)
    result = runner.invoke(create, [dataset_name, tmp_dir_fixture])
    assert result.exit_code == 0

    # Test that the dataset has been created.
    dataset_uri = sanitise_uri(dataset_path)
    dataset = ProtoDataSet.from_uri(dataset_uri)

    # Test that the dataset name is correct.
    assert dataset.name == dataset_name
