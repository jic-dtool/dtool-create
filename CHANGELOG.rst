CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.


[Unreleased]
------------

Added
^^^^^


Changed
^^^^^^^


Deprecated
^^^^^^^^^^


Removed
^^^^^^^


Fixed
^^^^^

- Deal with issue in how ruamel.yaml deals with float values


Security
^^^^^^^^

[0.19.0] - 2018-08-03
---------------------

Added
^^^^^

- Added ability to update the name of a frozen dataset


[0.18.0] - 2018-07-31
---------------------

Added
^^^^^

- Validation of dataset name upon creation
- Validation of dataset name when updating it


[0.17.0] - 2018-07-26
---------------------

Added
^^^^^

- Ability to update descriptive metadata in README of frozen datasets
- Validation that the descriptive metadata provided by the
  ``dtool readme edit`` command is valid YAML


[0.16.0] - 2018-06-06
---------------------

Added
^^^^^

- Pre-checks to 'dtool freeze' command to ensure that there is no rogue content
  in the base of disk datasets


[0.15.0] - 2018-05-18
---------------------

Added
^^^^^

- Pre-checks to 'dtool freeze' command to ensure that the item handles are sane, i.e. that they do not contain newline characters
- Pre-checks to 'dtool freeze' command to ensure that there are not too many items in the proto dataset, default to less than 10000


[0.14.0] - 2018-02-09
---------------------

Changed
^^^^^^^

- The path to the data when creating a symlink dataset is now specified using the
  ``-s/--symlink-path`` option rather than being something that is prompted for.
  This makes it easier to create symlink datasets in an automated fashion.



[0.13.0] - 2018-02-05
---------------------

Added
^^^^^

- ``--resume`` option to ``dtool copy`` command


[0.12.0] - 2018-01-18
---------------------

Changed
^^^^^^^

- Updated code to make use of dtoolcore version 3 API


[0.11.0] - 2017-12-14
---------------------

Added
^^^^^

- Ability to specify a custom README.yml template file path.
- Ability to configure the full user name for the README.yml template using
  ``DTOOL_USER_FULL_NAME``

Fixed
^^^^^

- Made the YAML output more pretty by adding more indentation.
- Replaced hardcoded ``nbi.ac.uk`` email with configurable ``DTOOL_USER_EMAIL``
  in the default README.yml template.


[0.10.0] - 2017-10-23
---------------------

Added
^^^^^

- ``--quiet`` flag to ``dtool create`` command

Changed
^^^^^^^

- ``dtool copy`` now specifies target location using URI rather than
  using the ``--prefix`` and ``--storage`` arguments

Fixed
^^^^^

- Made error handling in ``dtool create`` more specific
- Added propagation of original error message when ``StorageBrokerOSError``
  captures in ``dtool create``


[0.9.0] - 2017-10-04
--------------------

Added
^^^^^

- ``dtool readme show`` command that returns the readme content
- ``--quiet`` flag to ``dtool copy`` command


Changed
^^^^^^^

- Improved the ``dtool readme --help`` output


[0.8.0] - 2017-09-25
--------------------

Added
^^^^^

- Better validation of input in terms of base vs proto vs frozen dataset URIs


[0.7.0] - 2017-09-15
--------------------

Added
^^^^^

- ``dtool name`` command

Fixed
^^^^^

- Made distinction between proto dataset and dataset cleared in dtool help and feedback


[0.6.0] - 2017-09-13
--------------------

Added
^^^^^

- Progress bar to ``dtool freeze``
- Progress bar to ``dtool copy``

Fixed
^^^^^

- Made code Python 3 compatible


[0.5.0] - 2017-09-11
--------------------

Added
^^^^^

- ``dtool copy`` command
- Improved user feedback when creating a ``symlink`` dataset


[0.4.0] - 2017-09-05
--------------------

Added
^^^^^

- ``dtool add item`` command
- ``dtool add metadata`` command
- Configuration file support


Changed
^^^^^^^

- URI for DiskStorageBroker now assumed to be
  ``file:///some/path`` or ``/some/path``


[0.3.0] - 2017-09-01
--------------------

Added
^^^^^

- The ``dtool create`` now works with storage broker plugins

Fixed
^^^^^

- Make ``dtool create`` work with version 2.1 of the ``dtoolcore`` API


Security
^^^^^^^^


[0.2.0] - 2017-08-30
--------------------

Basic release with three commands that make use of the ``dtoolcore`` version
2 API and ``dtool-cli``. It provides three commands that plug into the
``dtool-cli`` version 0.2.0 ``dtool.cli`` entry point.

- ``create`` - for creating a new proto dataset
- ``readme`` - for editing the README.yml of the dataset
- ``freeze`` - for converting a proto dataset into a dataset
