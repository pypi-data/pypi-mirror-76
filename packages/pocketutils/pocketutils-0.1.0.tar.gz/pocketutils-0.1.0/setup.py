# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocketutils',
 'pocketutils.biochem',
 'pocketutils.core',
 'pocketutils.logging',
 'pocketutils.misc',
 'pocketutils.notebooks',
 'pocketutils.plotting',
 'pocketutils.tools']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL>=0,<1',
 'colorama>=0,<1',
 'dill>=0.3,<0.4',
 'goatools>=1,<2',
 'importlib-metadata>=1,<2',
 'ipython>=7',
 'joblib>=0,<1',
 'jsonpickle>=1,<2',
 'matplotlib>=3,<4',
 'natsort>=7,<8',
 'numpy>=1,<2',
 'pandas>=1,<2',
 'peewee>=3,<4',
 'psutil>=5,<6',
 'requests>=2,<3',
 'scikit-image>=0,<1',
 'scikit-learn>=0,<1',
 'scipy>=1,<2',
 'sshtunnel>=0,<1',
 'tomlkit>=0,<1',
 'typer>=0,<1',
 'uniprot>=1,<2',
 'urllib3[secure]>=1,<2']

setup_kwargs = {
    'name': 'pocketutils',
    'version': '0.1.0',
    'description': 'Adorable little Python code for you to copy or import.',
    'long_description': '# pocketutils\n\n[![Version status](https://img.shields.io/pypi/status/pocketutils)](https://pypi.org/project/pocketutils/)\n[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pocketutils)](https://pypi.org/project/pocketutils/)\n[![Docker](https://img.shields.io/docker/v/dmyersturnbull/pocketutils?color=green&label=DockerHub)](https://hub.docker.com/repository/docker/dmyersturnbull/pocketutils)\n[![GitHub release (latest SemVer including pre-releases)](https://img.shields.io/github/v/release/dmyersturnbull/pocketutils?include_prereleases&label=GitHub)](https://github.com/dmyersturnbull/pocketutils/releases)\n[![Latest version on PyPi](https://badge.fury.io/py/pocketutils.svg)](https://pypi.org/project/pocketutils/)\n[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/pocketutils?label=Conda-Forge)](https://anaconda.org/conda-forge/pocketutils)\n[![Documentation status](https://readthedocs.org/projects/pocketutils/badge/?version=latest&style=flat-square)](https://pocketutils.readthedocs.io/en/stable/)\n[![Build & test](https://github.com/dmyersturnbull/pocketutils/workflows/Build%20&%20test/badge.svg)](https://github.com/dmyersturnbull/pocketutils/actions)\n[![Travis](https://img.shields.io/travis/dmyersturnbull/pocketutils?label=Travis)](https://travis-ci.org/dmyersturnbull/pocketutils)\n[![Azure DevOps builds](https://img.shields.io/azure-devops/build/dmyersturnbull/<<key>>/<<defid>>?label=Azure)](https://dev.azure.com/dmyersturnbull/pocketutils/_build?definitionId=1&_a=summary)\n[![Maintainability](https://api.codeclimate.com/v1/badges/<<apikey>>/maintainability)](https://codeclimate.com/github/dmyersturnbull/pocketutils/maintainability)\n[![Coverage](https://coveralls.io/repos/github/dmyersturnbull/pocketutils/badge.svg?branch=master)](https://coveralls.io/github/dmyersturnbull/pocketutils?branch=master)\n\nAdorable little Python functions for you to copy or import.\n\nAmong the more useful are `zip_strict`, `frozenlist`, `SmartEnum`, `is_lambda`, `strip_paired_brackets`,\n`sanitize_path_node`, `TomlData`, `PrettyRecordFactory`, `parallel_with_cursor`, `groupby_parallel`,\n`loop_timing`, and `stream_cmd_call`.\n\nAlso has functions for plotting, machine learning, and bioinformatics.\nSome of the more useful are `ConfusionMatrix`, `DecisionFrame`,\n[`PeakFinder`](https://en.wikipedia.org/wiki/Topographic_prominence), `AtcParser` (for PubChem ATC codes),\n`WellBase1` (for multiwell plates), and [`TissueTable`]("https://www.proteinatlas.org/).\n\n[See the docs](https://littlesnippets.readthedocs.io/en/stable/), or just\n[browse the code](https://github.com/dmyersturnbull/littlesnippets/tree/master/littlesnippets).\n\n[New issues](https://github.com/dmyersturnbull/pocketutils/issues) and pull requests are welcome.\nPlease refer to the [contributing guide](https://github.com/dmyersturnbull/pocketutils/blob/master/CONTRIBUTING.md).\nGenerated with [Tyrannosaurus](https://github.com/dmyersturnbull/tyrannosaurus).\n',
    'author': 'Douglas Myers-Turnbull',
    'author_email': None,
    'maintainer': 'Douglas Myers-Turnbull',
    'maintainer_email': None,
    'url': 'https://github.com/dmyersturnbull/pocketutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
