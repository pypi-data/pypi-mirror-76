# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextfilter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'contextfilter',
    'version': '0.1.1',
    'description': 'ContextVars Filter for easily enriching log records',
    'long_description': None,
    'author': 'Aviram Hassan',
    'author_email': 'aviramyhassan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
