# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dddroller']

package_data = \
{'': ['*']}

install_requires = \
['snregales>=0.2.0,<0.3.0']

extras_require = \
{'docs': ['sphinx_rtd_theme>=0.5.0,<0.6.0'],
 'lint': ['flake8-isort==3.0.0', 'isort>=4.3.20,<5.0.0'],
 'local': ['pytest-cov>=2.9.0,<3.0.0',
           'flake8-isort==3.0.0',
           'isort>=4.3.20,<5.0.0',
           'sphinx_rtd_theme>=0.5.0,<0.6.0'],
 'test': ['pytest-cov>=2.9.0,<3.0.0']}

setup_kwargs = {
    'name': 'dddroller',
    'version': '0.1.0',
    'description': 'Dungeon and Dragons Dice Roller',
    'long_description': '.. Badges Alias End\n\n|Build Status|\n\n.. Badges Alias Start\n\n---\n\n.. Badges Start\n\n.. |Build Status| image:: https://img.shields.io/gitlab/pipeline/presentations4/dddroller/master\n   :alt: Gitlab pipeline status\n   :target: https://gitlab.com/presentations4/dddroller/commits/master\n\n.. Badges End\n',
    'author': 'Sharlon Regales',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
