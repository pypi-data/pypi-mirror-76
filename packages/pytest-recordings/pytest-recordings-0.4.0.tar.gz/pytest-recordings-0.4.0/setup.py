# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_recordings', 'pytest_recordings.decorators']

package_data = \
{'': ['*']}

install_requires = \
['vcrpy==4.0.2']

entry_points = \
{'pytest11': ['pytest_recordings = pytest_recordings.hooks']}

setup_kwargs = {
    'name': 'pytest-recordings',
    'version': '0.4.0',
    'description': 'Provides pytest plugins for reporting request/response traffic, screenshots, and more to ReportPortal',
    'long_description': None,
    'author': 'Jonathan Castillo',
    'author_email': 'jonathan.castillo@cloudcheckr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
