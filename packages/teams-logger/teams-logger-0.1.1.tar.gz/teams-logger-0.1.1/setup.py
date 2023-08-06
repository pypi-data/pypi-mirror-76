# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teams_logger']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'teams-logger',
    'version': '0.1.1',
    'description': 'Microsoft Teams logging handler fot Python',
    'long_description': None,
    'author': 'Anes Foufa',
    'author_email': 'anes.foufa@upply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
