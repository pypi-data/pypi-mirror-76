# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reqs']

package_data = \
{'': ['*'],
 'reqs': ['.mypy_cache/3.7/*',
          '.mypy_cache/3.7/asyncio/*',
          '.mypy_cache/3.7/collections/*',
          '.mypy_cache/3.7/concurrent/*',
          '.mypy_cache/3.7/concurrent/futures/*',
          '.mypy_cache/3.7/ctypes/*',
          '.mypy_cache/3.7/email/*',
          '.mypy_cache/3.7/http/*',
          '.mypy_cache/3.7/httpx/*',
          '.mypy_cache/3.7/httpx/backends/*',
          '.mypy_cache/3.7/httpx/dispatch/*',
          '.mypy_cache/3.7/importlib/*',
          '.mypy_cache/3.7/json/*',
          '.mypy_cache/3.7/logging/*',
          '.mypy_cache/3.7/multiprocessing/*',
          '.mypy_cache/3.7/os/*',
          '.mypy_cache/3.7/urllib/*']}

entry_points = \
{'console_scripts': ['reqs = reqs.reqs:main']}

setup_kwargs = {
    'name': 'reqs',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Kirill Plotnikov',
    'author_email': 'init@pltnk.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
