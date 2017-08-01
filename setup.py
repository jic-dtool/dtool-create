from setuptools import setup

url = ""
version = "0.1.0"
readme = open('README.rst').read()

setup(
    name="dtool-create",
    packages=["dtool_create"],
    version=version,
    description="Dtool plugin for creating datasets and collections",
    long_description=readme,
    include_package_data=True,
    author="Tjelvar Olsson",
    author_email="tjelvar.olsson@jic.ac.uk",
    url=url,
    install_requires=[
        "Click",
        "dtoolcore",
    ],
    entry_points={
        "dtool.dataset": [
            "create=dtool_create.dataset:create",
        ],
    },
    download_url="{}/tarball/{}".format(url, version),
    license="MIT"
)
