# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snf_simple']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.1,<2.0.0', 'scikit-learn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'snf-simple',
    'version': '0.1.1',
    'description': 'Similarity Network Fusion (SNF) python implementation',
    'long_description': '# Similarity Network Fusion (SNF)\nSNF python implementation with intention to be 1-2 with MatlabV 2.1\n\nReference:\n\n> B Wang, A Mezlini, F Demir, M Fiume, T Zu, M Brudno, B Haibe-Kains, A Goldenberg (2014) Similarity Network Fusion: a fast and effective method to aggregate multiple data types on a genome wide scale. Nature Methods. Online. Jan 26, 2014\n\n## Usage\nInstall from pypi:\n```shell script\npip install snf_simple\n```\n\n\n\n## Using the module\nYou can see an example usage under [demo](./examples/demo.py)\n\n## Development\nThe project is using [poetry](https://python-poetry.org/) for reliable development.\n\nSee poetry documentation on how to install the latest version for your system:\n\n> https://python-poetry.org/docs\n\n### Setup\nAfter installing poetry, start an environment:\n\n```shell script\npoetry install\n```\n\nIf you are using PyCharm you can use [this plugin](https://plugins.jetbrains.com/plugin/14307-poetry) for setting up interpreter.\n\n### Testing\nTests are using standard `pytest` format. You can run them after the setup with:\n\n```shell script\npytest\n```\n',
    'author': 'fmakdemir',
    'author_email': 'fmakdemir@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fmakdemir/snf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
