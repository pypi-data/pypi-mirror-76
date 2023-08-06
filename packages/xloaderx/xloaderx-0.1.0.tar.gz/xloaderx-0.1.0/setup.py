# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xloaderx']

package_data = \
{'': ['*'], 'xloaderx': ['.idea/*', '.idea/inspectionProfiles/*']}

setup_kwargs = {
    'name': 'xloaderx',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mjaquier',
    'author_email': 'mjaquier@admin.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
