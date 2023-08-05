# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmlparsert']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'htmlparsert',
    'version': '0.1.0',
    'description': 'A lightweight, no dependency HTML parser for text processing',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
