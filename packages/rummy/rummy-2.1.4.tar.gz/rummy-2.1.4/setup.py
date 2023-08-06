# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rummy',
 'rummy.constants',
 'rummy.controller',
 'rummy.deck',
 'rummy.exception',
 'rummy.game',
 'rummy.player',
 'rummy.ui',
 'rummy.view']

package_data = \
{'': ['*'], 'rummy': ['templates/*']}

install_requires = \
['Pygments==2.2.0',
 'ansi-colours==0.2.6',
 'codecov==2.0.15',
 'colorama==0.4.0',
 'coverage==4.5.1',
 'more-itertools==4.3.0',
 'pytest-cov==2.6.0',
 'pytest-mock==1.10.0',
 'pytest==3.10.0',
 'text-template==0.1.4']

entry_points = \
{'console_scripts': ['rummy = rummy.__main__:main']}

setup_kwargs = {
    'name': 'rummy',
    'version': '2.1.4',
    'description': 'Console Rummy game',
    'long_description': None,
    'author': 'Sarcoma',
    'author_email': 'sean@orderandchaoscreative.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
