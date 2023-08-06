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
    'version': '0.1.0',
    'description': 'Similarity Network Fusion (SNF) python implementation',
    'long_description': None,
    'author': 'fmakdemir',
    'author_email': 'fmakdemir@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
