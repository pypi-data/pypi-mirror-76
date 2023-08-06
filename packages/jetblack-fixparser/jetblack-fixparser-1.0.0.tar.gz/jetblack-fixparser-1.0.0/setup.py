# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jetblack_fixparser',
 'jetblack_fixparser.fix_message',
 'jetblack_fixparser.loader',
 'jetblack_fixparser.meta_data']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.16.10,<0.17.0', 'wheel>=0.34.2,<0.35.0']

setup_kwargs = {
    'name': 'jetblack-fixparser',
    'version': '1.0.0',
    'description': 'A parser for FIX messages',
    'long_description': None,
    'author': 'Rob Blackbourn',
    'author_email': 'rob.blackbourn@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rob-blackbourn/jetblack-fixparser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
