# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['schema_renderer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'schema-renderer',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
