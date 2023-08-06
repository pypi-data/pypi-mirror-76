# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aer',
    'version': '0.1.0',
    'description': 'A CLI helper for using EMR on AWS',
    'long_description': '# aer\nA CLI helper for using [EMR](https://aws.amazon.com/emr/) on AWS\n',
    'author': 'Joseph Egan',
    'author_email': 'joseph.s.egan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eganjs/aer',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
