# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['oddysey']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'oddysey',
    'version': '0.1.0',
    'description': 'A yet unknown accompanying project for iliad',
    'long_description': '# oddysey\nA yet unknown accompanying project for [iliad](https://github.com/eganjs/iliad)\n',
    'author': 'Joseph Egan',
    'author_email': 'joseph.s.egan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eganjs/oddysey',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
