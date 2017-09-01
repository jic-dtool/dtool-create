"""dataset command line module."""

import sys
import os
import getpass
import datetime

from StringIO import StringIO

import click
import dtoolcore

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


README_TEMPLATE = """---
description: Dataset description
project: Project name
confidential: False
personally_identifiable_information: False
owners:
  - name: Your Name
    email: {username}@nbi.ac.uk
    username: {username}
creation_date: {date}
# links:
#  - http://doi.dx.org/your_doi
#  - http://github.com/your_code_repository
# budget_codes:
#  - E.g. CCBS1H10S
""".format(username=getpass.getuser(), date=datetime.date.today())


def create_path(ctx, param, value):
    abspath = os.path.abspath(value)
    if os.path.exists(abspath):
        raise click.BadParameter(
            "File/directory already exists: {}".format(abspath))
    return abspath


def dataset_uri_validation(ctx, param, value):
    if not dtoolcore._is_dataset(value, config=None):
        raise click.BadParameter(
            "URI is not a dataset: {}".format(value))
    return value


def storagebroker_validation(ctx, param, value):
    storage_broker_lookup = dtoolcore._generate_storage_broker_lookup()
    if value not in storage_broker_lookup:
        raise click.BadParameter(
            "'{}' not in {}".format(value, storage_broker_lookup.keys()))
    return value

dataset_uri_argument = click.argument(
    "dataset_uri",
    callback=dataset_uri_validation
)


@click.command()
@click.argument("name")
@click.argument("prefix", default="")
@click.argument("storage", default="disk", callback=storagebroker_validation)
def create(name, storage, prefix):
    """Create an empty dataset."""
    admin_metadata = dtoolcore.generate_admin_metadata(name)
    dataset_uuid = admin_metadata["uuid"]

    # Get the right storage broker and use it to generate a URI.
    storage_broker_lookup = dtoolcore._generate_storage_broker_lookup()
    storage_broker = storage_broker_lookup[storage]
    dataset_uri = storage_broker.generate_uri(name, dataset_uuid, prefix)

    # Create the dataset.
    proto_dataset = dtoolcore.ProtoDataSet(
        uri=dataset_uri,
        admin_metadata=admin_metadata,
        config=None)
    try:
        proto_dataset.create()
    except:
        raise click.UsageError(
            "'{}' already exists: {}".format(
                name, dataset_uri))

    proto_dataset.put_readme("")

    # Find the abspath of the data directory for user feedback.
    data_path = proto_dataset._storage_broker._data_abspath

    # Give the user some feedback and hints on what to do next.
    click.secho("Created dataset ", nl=False, fg="green")
    click.secho(dataset_uri)
    click.secho("Next steps: ")
    click.secho("1. Add descriptive metadata, e.g: ")
    click.secho(
        "dtool readme interactive {}".format(dataset_uri),
        fg="cyan")
    click.secho("2. Add raw data, e.g: ")
    click.secho("mv my_data_directory {}/".format(data_path), fg="cyan")
    click.secho("3. Freeze the dataset: ")
    click.secho("dtool freeze {}".format(dataset_uri), fg="cyan")


@click.group()
def readme():
    """Add descriptive metadata to the readme.
    """


@readme.command()
@dataset_uri_argument
def interactive(dataset_uri):
    """Update the readme file interactively."""
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(dataset_uri)

    # Create an CommentedMap representation of the yaml readme template.
    yaml = YAML()
    yaml.explicit_start = True
    descriptive_metadata = yaml.load(README_TEMPLATE)

    def prompt_for_values(d):
        """Update the descriptive metadata interactively.

        Uses values entered by the user. Note that the function keeps recursing
        whenever a value is another ``CommentedMap`` or a ``list``. The
        function works as passing dictionaries and lists into a function edits
        the values in place.
        """
        for key, value in d.items():
            if isinstance(value, CommentedMap):
                prompt_for_values(value)
            elif isinstance(value, list):
                for item in value:
                    prompt_for_values(item)
            else:
                new_value = click.prompt(key, type=type(value), default=value)
                d[key] = new_value

    prompt_for_values(descriptive_metadata)

    # Write out the descriptive metadata to the readme file.
    stream = StringIO()
    yaml.dump(descriptive_metadata, stream)
    proto_dataset.put_readme(stream.getvalue())

    click.secho("Updated readme ", fg="green")
    click.secho("To edit the readme using your default editor:")
    click.secho(
        "dtool readme edit {}".format(dataset_uri),
        fg="cyan")


@readme.command()
@dataset_uri_argument
def edit(dataset_uri):
    """Edit the readme file with your default editor.
    """
    proto_dataset = dtoolcore.ProtoDataSet.from_uri(dataset_uri)
    readme_content = proto_dataset.get_readme_content()
    edited_content = click.edit(readme_content)
    if edited_content is not None:
        proto_dataset.put_readme(edited_content)
        click.secho("Updated readme ", nl=False, fg="green")
    else:
        click.secho("Did not update readme ", nl=False, fg="red")
    click.secho(dataset_uri)


@click.command()
@dataset_uri_argument
def freeze(dataset_uri):
    """Finalise a dataset.

    This step is carried out after all files have been added to the dataset.
    Freezing a dataset finalizes it with a stamp marking it as frozen.
    """
    try:
        proto_dataset = dtoolcore.ProtoDataSet.from_uri(dataset_uri)
    except dtoolcore.DtoolCoreTypeError:
        try:
            dataset = dtoolcore.DataSet.from_uri(dataset_uri)
            click.secho("Dataset is already frozen at ", nl=False)
            timestamp = float(dataset._admin_metadata["frozen_at"])
            dt = datetime.datetime.fromtimestamp(timestamp)
            click.secho(dt.strftime('%Y-%m-%d %H:%M:%S UTC'))
        finally:
            sys.exit()
    proto_dataset.freeze()
    click.secho("Dataset frozen ", nl=False, fg="green")
    click.secho(dataset_uri)
