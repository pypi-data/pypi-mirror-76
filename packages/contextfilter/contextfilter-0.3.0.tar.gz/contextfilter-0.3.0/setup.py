# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['contextfilter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'contextfilter',
    'version': '0.3.0',
    'description': 'ContextVars Filter for easily enriching log records',
    'long_description': '# contextfilter\n![Version](https://img.shields.io/pypi/v/contextfilter)\n![License](https://img.shields.io/pypi/l/contextfilter)\n![Tests](https://github.com/aviramha/contextfilter/workflows/Test%20Contextfilter/badge.svg?branch=develop)\n\nSmall, helper library for logging contextual information using contextvars in Python 3.7.\n\n## Installation\nUsing pip\n```\n$ pip install contextfilter\n```\n\n## Usage\n```py\nimport logging\nfrom contextvars import ContextVar\nfrom contextfilter import ContextVarFilter, ConstContextFilter\n\nrequest_id: ContextVar[int] = ContextVar(\'request_id\')\nlogger = logging.getLogger("test")\ncf = ContextFilter(request_id=request_id)\nrequest_id.set(3)\nlogger.addFilter(cf)\nlogger.info("test")\n# Log record will contain the attribute request_id with value 3\n\ncf = ConstContextFilter(some_const=1)\nlogger.addFilter(cf)\nlogger.info("test")\n# Log record will contain the attribute some_const with value 1.\n\n```\n\n## Contributing\n\nTo work on the `contextfilter` codebase, you\'ll want to fork the project and clone it locally and install the required dependencies via [poetry](https://poetry.eustace.io):\n\n```sh\n$ git clone git@github.com:{USER}/contextfilter.git\n$ make install\n```\n\nTo run tests and linters use command below:\n\n```sh\n$ make lint && make test\n```\n\nIf you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:\n\n```sh\n$ make lint-black\n```\n\n## License\n\n`contextfilter` is licensed under the MIT license. See the license file for details.\n\n# Latest changes\n\n## 0.3.0 (2020-8-14)\n- Renamed `ContextFilter` to `ContextVarFilter` - Revamped the API - It now accepts ContextVars created by caller. Suggestion for design by @bentheiii\n- Added `ConstContextFilter` which adds constant attributes to the log record.\n- Fixed #5',
    'author': 'Aviram Hassan',
    'author_email': 'aviramyhassan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aviramha/contextfilter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
