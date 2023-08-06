# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaml2jsonnet']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['yaml2jsonnet = yaml2jsonnet']}

setup_kwargs = {
    'name': 'yaml2jsonnet',
    'version': '0.6.0',
    'description': 'Convert from YAML to Jsonnet format, retaining comments',
    'long_description': "=================\nyaml2jsonnet\n=================\n\n\nConverts YAML into Jsonnet (specifically targetting YAML for Kubernetes)\n\nSuppose that you have some `YAML`_ that you use for `Kubernetes`_ (either hand-written or output by `Helm`_. Now you'd like to use\n`Jsonnet`_ instead, for its fancier templating capabilities. This is a pain, because while YAML->JSON converters are easy to find,\nthey produce ugly-looking (but valid!) Jsonnet.\n\nThe goal of this project is to make the conversion a little easier: transform the YAML into *slightly* prettier Jsonnet, preserving\ncomments along the way.\n\n\n------------------\nDevelopment Setup\n------------------\n\n\n* Install `Poetry`_\n* Install `Pre-commit`_\n* Run ``poetry install`` to install dependencies\n* Run ``poetry run python -m yaml2jsonnet /path/to/yaml`` to convert a file\n* Probably, run ``jsonnetfmt`` on the output, since the only whitespace I provide is newlines\n\n\n\n.. _YAML: https://yaml.org/\n.. _Helm: https://helm.sh/\n.. _Jsonnet: https://jsonnet.org/\n.. _Kubernetes: https://kubernetes.io/\n.. _Poetry: https://python-poetry.org/\n.. _Pre-commit: https://pre-commit.com/\n",
    'author': 'Nathaniel Waisbrot',
    'author_email': 'code@waisbrot.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/waisbrot/yaml2jsonnet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
