"""dataset command line module."""

import os

import click
import dtoolcore

from dtool_cli.cli import dataset_path_argument


def create_path(ctx, param, value):
    abspath = os.path.abspath(value)
    if os.path.exists(abspath):
        raise click.BadParameter(
            "File/directory already exists: {}".format(abspath))
    os.mkdir(abspath)
    return abspath


@click.command()
@click.argument("new_dataset_path", callback=create_path)
def create(new_dataset_path):
    """Create an empty dataset."""
    dataset_name = os.path.basename(new_dataset_path)
    dataset = dtoolcore.DataSet(dataset_name, data_directory="data")
    dataset.persist_to_path(new_dataset_path)
    click.secho("Created dataset: {}".format(new_dataset_path))


@click.command()
@dataset_path_argument
def freeze(dataset_path):
    """Finalise a dataset.

    This step is carried out after all files have been added to the dataset.
    Freezing a dataset finalizes it with a stamp marking it as frozen.
    """
    dataset = dtoolcore.DataSet.from_path(dataset_path)
    dataset.update_manifest()
    # dataset.freeze()
    click.secho("Dataset frozen")
