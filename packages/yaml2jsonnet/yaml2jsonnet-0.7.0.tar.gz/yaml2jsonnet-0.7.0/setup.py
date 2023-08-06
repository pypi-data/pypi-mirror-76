# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yaml2jsonnet']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['yaml2jsonnet = yaml2jsonnet.cli:main']}

setup_kwargs = {
    'name': 'yaml2jsonnet',
    'version': '0.7.0',
    'description': 'Convert from YAML to Jsonnet format, retaining comments',
    'long_description': "# YAML2Jsonnet: Switch configuration languages\n\nConverts YAML into Jsonnet (specifically targetting YAML for Kubernetes)\n\nSuppose that you have some [YAML][] that you use for [Kubernetes][] (either hand-written or output by [Helm][]. Now you'd like to use\n[Jsonnet][] instead, for its fancier templating capabilities. This is a pain, because while YAML->JSON converters are easy to find,\nthey produce ugly-looking (but valid!) Jsonnet.\n\nYAML2Jsonnet makes the conversion a little easier: it transforms the YAML into *slightly* prettier Jsonnet, preserving\ncomments along the way.\n\n## Examples\n\nTODO\n\n## Development\n\n* Install [Poetry]\n* Install [Pre-commit]\n* Run `poetry install` to install dependencies\n* Run `poetry run python -m yaml2jsonnet /path/to/yaml` to convert a file\n* Probably, run `jsonnetfmt` on the output, since the only whitespace I provide is newlines\n\n\n[YAML]: https://yaml.org/\n[Helm]: https://helm.sh/\n[Jsonnet]: https://jsonnet.org/\n[Kubernetes]: https://kubernetes.io/\n[Poetry]: https://python-poetry.org/\n[Pre-commit]: https://pre-commit.com/\n",
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
