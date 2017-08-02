"""Test the ``dtool dataset create`` command."""

import os
import shutil

from click.testing import CliRunner

from dtoolcore import DataSet

from . import chdir_fixture, tmp_dir_fixture  # NOQA
from . import SAMPLE_FILES_DIR


def test_dataset_freeze_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import freeze
    runner = CliRunner()

    # Create an empty dataset
    dataset_name = "my_dataset"
    dataset = DataSet(dataset_name, data_directory="data")
    dataset.persist_to_path(".")

    # Add some files to it.
    dest_dir = os.path.join(".", dataset.data_directory, "sample_files")
    shutil.copytree(SAMPLE_FILES_DIR, dest_dir)

    # At this point the manifest has not been updated.
    assert len(dataset.identifiers) == 0

    result = runner.invoke(freeze, ["."])
    assert result.exit_code == 0

    # Manifest has been updated.
    assert len(dataset.identifiers) == 2
