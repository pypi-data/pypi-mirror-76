# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['listview']
setup_kwargs = {
    'name': 'listview',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
