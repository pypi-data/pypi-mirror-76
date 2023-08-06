#!/usr/bin/env python

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

from dilldb import __author__, __version__, __email__

setup(name="dilldb",
     version='.'.join([str(v) for v in __version__]),
     description="key value database with json or pickle format",
     author=__author__,
     author_email=__email__,
     packages=find_packages(),
     include_package_data=True,
     install_requires=["setuptools", "dill"],
     py_modules=['dilldb'],
     project_urls={
        'Documentations': 'http://lj25fp.asux-ae-ai-gitlab.aptiv.today/dilldb',
        'Source': 'https://github.com/afeldman/dilldb',
        'Tracker': 'https://github.com/afeldman/dilldb/issues'
     },
)