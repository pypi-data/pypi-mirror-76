# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aer', 'aer.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['aer = aer.cli:cli']}

setup_kwargs = {
    'name': 'aer',
    'version': '0.2.0',
    'description': 'A CLI helper for using EMR on AWS',
    'long_description': '# aer\nA CLI helper for using [EMR](https://aws.amazon.com/emr/) on AWS\n',
    'author': 'Joseph Egan',
    'author_email': 'joseph.s.egan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eganjs/aer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
