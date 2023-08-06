# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['feature_change']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'feature-change',
    'version': '0.1.0',
    'description': 'Feature Change helps you check if a new function behaves like and older one',
    'long_description': None,
    'author': "Felipe 'Bidu' Rodrigues",
    'author_email': 'felipe@felipevr.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
