"""Test the ``dtool dataset copy`` command."""

import os

from click.testing import CliRunner

from dtoolcore import DataSet, ProtoDataSet
from dtoolcore.compare import diff_content

from . import chdir_fixture, tmp_dir_fixture  # NOQA


def test_dataset_copy_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create, freeze, add, copy
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    # At this point we have a proto dataset
    dataset_abspath = os.path.abspath(dataset_name)
    dataset_uri = "file://{}".format(dataset_abspath)
    dataset = ProtoDataSet.from_uri(dataset_uri)

    # Create a directory to copy the dataset to.
    copy_directory = os.path.abspath("copy_dir")
    os.mkdir(copy_directory)

    # It should not be possible to copy a proto dataset.
    result = runner.invoke(copy, [dataset_uri, copy_directory])
    assert result.exit_code != 0

    # Create sample file to the proto dataset.
    sample_file_name = "hello.txt"
    with open(sample_file_name, "w") as fh:
        fh.write("hello world")

    # Put it into the dataset
    result = runner.invoke(add, ["item", sample_file_name, dataset_uri])
    assert result.exit_code == 0

    result = runner.invoke(freeze, [dataset_uri])
    assert result.exit_code == 0

    # Now we have a dataset.
    dataset = DataSet.from_uri(dataset_uri)

    # It should now be possible to copy the dataset.
    result = runner.invoke(copy, [dataset_uri, copy_directory])
    assert result.exit_code == 0

    # However, it cannot be done again.
    result = runner.invoke(copy, [dataset_uri, copy_directory])
    assert result.exit_code != 0
    assert result.output.find("Error: Dataset already exists") != -1

    # Create another directory to copy the dataset to.
    copy_directory_2 = os.path.abspath("copy_dir_2")
    os.mkdir(copy_directory_2)

    # Test the quite flag.
    result = runner.invoke(copy, ["--quiet", dataset_uri, copy_directory_2])
    assert result.exit_code == 0
    expected_uri = "file://" + os.path.join(copy_directory_2, dataset_name)
    assert result.output.strip() == expected_uri

    # Compare the content of the two datasets.
    copied_dataset = DataSet.from_uri(expected_uri)
    assert len(diff_content(dataset, copied_dataset)) == 0
