"""Test the ``dtool name`` command."""

import os

from . import chdir_fixture  # NOQA

from click.testing import CliRunner

from dtoolcore import ProtoDataSet
from dtoolcore.utils import sanitise_uri


def test_dataset_name_functional(chdir_fixture):  # NOQA
    from dtool_create.dataset import create, name, freeze
    runner = CliRunner()

    dataset_name = "my_dataset"
    result = runner.invoke(create, [dataset_name])
    assert result.exit_code == 0

    dataset_abspath = os.path.abspath(dataset_name)
    dataset_uri = sanitise_uri(dataset_abspath)

    # Test that the proto dataset has been created.
    dataset = ProtoDataSet.from_uri(dataset_uri)

    # Test that the dataset name is correct.
    assert dataset.name == dataset_name

    result = runner.invoke(name, [dataset_uri])
    assert result.exit_code == 0
    assert result.output.strip() == "my_dataset"

    result = runner.invoke(name, [dataset_uri, "new_name"])
    assert result.exit_code == 0
    assert result.output.strip() == "new_name"

    result = runner.invoke(freeze, [dataset_uri])

    result = runner.invoke(name, [dataset_uri])
    assert result.exit_code == 0
    assert result.output.strip() == "new_name"

    result = runner.invoke(name, [dataset_uri, "frozen_ds_now_allowed"])
    assert result.output.strip() == "frozen_ds_now_allowed"
