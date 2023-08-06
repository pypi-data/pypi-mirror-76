# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytorch_resample']

package_data = \
{'': ['*']}

install_requires = \
['torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'pytorch-resample',
    'version': '0.1.0',
    'description': 'Resampling methods for iterable datasets in PyTorch',
    'long_description': None,
    'author': 'Max Halford',
    'author_email': 'maxhalford25@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
