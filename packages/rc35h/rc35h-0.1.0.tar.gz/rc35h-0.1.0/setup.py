# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rc35h']

package_data = \
{'': ['*']}

install_requires = \
['pysocks>=1.7.1,<2.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['rc35h = rc35h:main']}

setup_kwargs = {
    'name': 'rc35h',
    'version': '0.1.0',
    'description': 'Python RCE Shell',
    'long_description': None,
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
