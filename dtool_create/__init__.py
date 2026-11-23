"""dtool-create package."""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("dtool-create")
except PackageNotFoundError:
    # Package is not installed.
    __version__ = "unknown"
