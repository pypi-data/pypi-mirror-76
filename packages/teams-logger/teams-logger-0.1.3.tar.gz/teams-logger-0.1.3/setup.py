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
    'version': '0.1.3',
    'description': 'Microsoft Teams logging handler for Python',
    'long_description': "teams-logger\n===================\n\nPython logging handler for Microsoft Teams web hook integration with simple configuration.\n\nInstallation\n------------\n.. code-block:: bash\n\n    pip install teams-logger\n\nExample\n-------\nSimple\n''''''\n.. code-block:: python\n\n  import logging\n  from teams_handler import TeamsHandler\n\n  th = TeamsHandler(url='YOUR_WEB_HOOK_URL', level=logging.INFO)\n  logging.basicConfig(handlers=[sh])\n  logging.warning('warn message')\n\nUsing logger\n''''''''''''\n.. code-block:: python\n\n  import logging\n  from teams_handler import TeamsHandler\n\n  logger = logging.getLogger(__name__)\n  logger.setLevel(logging.DEBUG)\n\n  th = TeamsHandler(url='YOUR_WEB_HOOK_URL', level=logging.INFO)\n  sh.setLevel(logging.DEBUG)\n\n  logger.debug('debug message')\n  logger.info('info message')\n  logger.warn('warn message')\n  logger.error('error message')\n  logger.critical('critical message')\n",
    'author': 'Anes Foufa',
    'author_email': 'anes.foufa@upply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/AnesFoufa/python-teams-logger',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
