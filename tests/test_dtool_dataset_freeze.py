"""Test the ``dtool dataset create`` command."""

import os

from click.testing import CliRunner

from dtoolcore import DataSet, ProtoDataSet

from . import chdir_fixture, tmp_dir_fixture  # NOQA


def test_dataset_freeze_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create, freeze
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    # At this point we have a proto dataset
    dataset_abspath = os.path.abspath(dataset_name)
    dataset_uri = "disk:{}".format(dataset_abspath)
    dataset = ProtoDataSet.from_uri(dataset_uri)

    # Add a file to the proto dataset.
    sample_file_abspath = os.path.join(dataset_abspath, "data", "hello.txt")
    with open(sample_file_abspath, "w") as fh:
        fh.write("hello world")

    result = runner.invoke(freeze, [dataset_uri])
    assert result.exit_code == 0

    # Now we have a dataset.
    dataset = DataSet.from_uri(dataset_uri)

    # Manifest has been updated.
    assert len(dataset.identifiers) == 1
