# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postgrest_py']

package_data = \
{'': ['*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0', 'httpx>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'postgrest-py',
    'version': '0.2.0',
    'description': 'PostgREST client for Python. This library provides an ORM interface to PostgREST.',
    'long_description': None,
    'author': 'Lương Quang Mạnh',
    'author_email': 'luongquangmanh85@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
