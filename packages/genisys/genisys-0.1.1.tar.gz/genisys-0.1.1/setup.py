# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genisys', 'genisys.console', 'genisys.utils']

package_data = \
{'': ['*'], 'genisys.console': ['templates/*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.3,<0.5.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['genisys = genisys.console:genisys_cli'],
 'genisys.cli': ['create = genisys.console.create:create_cli',
                 'init = genisys.console.init:init_cli']}

setup_kwargs = {
    'name': 'genisys',
    'version': '0.1.1',
    'description': 'A framework for building intelligent microservices',
    'long_description': None,
    'author': 'David Lee',
    'author_email': 'ltw_david@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
