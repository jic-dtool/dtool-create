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


Security
^^^^^^^^


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
