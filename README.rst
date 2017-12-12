README
======

Dtool plugin for creating datasets.


Installation
------------

.. code-block:: bash

    pip install dtool-create

.. warning:: In order to be able to install the ``ryamel.yaml``
             dependency you may need to run::

                pip install -U pip setuptools wheel

             See http://yaml.readthedocs.io/en/latest/install.html
             for more details.


Usage
-----

Create a proto dataset::

    dtool create my_dataset

Add some data to to the dataset::

    cp *.csv my_dataset/data

Add descriptive metadata to the dataset::

    dtool readme interative my_dataset

Convert the proto dataset to a dataset by freezing it::

    dtool freeze my_dataset

See the `dtool documentation <http://dtool.readthedocs.io>`_ for more detail.


Configuring the descriptive metadata template
---------------------------------------------

It is possible to configure the required metadata prompted for by the
``dtool readme interactive`` command. The default template is the
``dtool_create/templates/README.yml``.

One may want to create a custom YAML file specifying the required metadata
that will be prompted for. This can be achieved by setting the
``DTOOL_README_TEMPLATE_FPATH`` environment variable, e.g.::

    export DTOOL_README_TEMPLATE_FPATH=~/dtool_readme.yml

Alternatively, one can add the ``DTOOL_README_TEMPLATE_FPATH`` key to the
``~/.config/dtool/dtool.json`` file.  For example,

.. code-block:: json

    {
       "DTOOL_README_TEMPLATE_FPATH": "/Users/olssont/dtool_readme.yml"
    }

If the ``~/.config/dtool/dtool.json`` file does not exist one may need to
create it.


Configuring the descriptive metadata email suffix
-------------------------------------------------

When running the ``dtool interactive readme`` the default behaviour is
provides an email address along the lines of ``username@``. It is possible
to add a suffix to this email address by setting the ``DTOOL_EMAIL_SUFFIX``
environment variable.

::

    export DTOOL_EMAIL_SUFFIX=nbi.ac.uk

Alternatively, one can add the ``DTOOL_README_TEMPLATE_FPATH`` key to the
``~/.config/dtool/dtool.json`` file.  For example,

.. code-block:: json

    {
       "DTOOL_EMAIL_SUFFIX": "nbi.ac.uk"
    }

If the ``~/.config/dtool/dtool.json`` file does not exist one may need to
create it.
