# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['play_checkers']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['play_checkers = play_checkers.__main__:main']}

setup_kwargs = {
    'name': 'play-checkers',
    'version': '1.0.5',
    'description': 'Python Checkers Game',
    'long_description': None,
    'author': 'Sarcoma',
    'author_email': 'sarcoma@live.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
