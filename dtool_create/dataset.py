"""dataset command line module."""

import os

import click
import dtoolcore


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
    dataset_name = os.path.basename(new_dataset_path)
    dataset = dtoolcore.DataSet(dataset_name, data_directory="data")
    dataset.persist_to_path(new_dataset_path)
    click.secho("Created dataset: {}".format(new_dataset_path))
