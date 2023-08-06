# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkkm_mr']

package_data = \
{'': ['*']}

install_requires = \
['cvxopt>=1.2.5,<2.0.0', 'numpy>=1.19.1,<2.0.0', 'scipy>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'mkkm-mr',
    'version': '0.2.3',
    'description': 'MKKM-MR Python Implementation',
    'long_description': None,
    'author': 'Fma',
    'author_email': 'fmakdemir@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
