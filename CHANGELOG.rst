CHANGELOG
=========

This project uses `semantic versioning <http://semver.org/>`_.
This change log uses principles from `keep a changelog <http://keepachangelog.com/>`_.

[Unreleased]
------------

Added
^^^^^

- ``dtool add item`` command
- ``dtool add metadata`` command


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


[0.3.0] 2017-09-01
------------------

Added
^^^^^

- The ``dtool create`` now works with storage broker plugins

Fixed
^^^^^

- Make ``dtool create`` work with version 2.1 of the ``dtoolcore`` API


Security
^^^^^^^^


[0.2.0] 2017-08-30
------------------

Basic release with three commands that make use of the ``dtoolcore`` version
2 API and ``dtool-cli``. It provides three commands that plug into the
``dtool-cli`` version 0.2.0 ``dtool.cli`` entry point.

- ``create`` - for creating a new proto dataset
- ``readme`` - for editing the README.yml of the dataset
- ``freeze`` - for converting a proto dataset into a dataset
