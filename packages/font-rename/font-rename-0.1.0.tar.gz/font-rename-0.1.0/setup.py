# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['font_rename']
install_requires = \
['cchardet>=2.1.4,<3.0.0', 'fonttools>=4.0.2,<5.0.0']

entry_points = \
{'console_scripts': ['font-rename = font_rename:main']}

setup_kwargs = {
    'name': 'font-rename',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whtsky/font-rename/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
