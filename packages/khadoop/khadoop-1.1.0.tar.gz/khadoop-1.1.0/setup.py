# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['khadoop', 'khadoop.yarn']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=0.15.8,<0.16.0']

setup_kwargs = {
    'name': 'khadoop',
    'version': '1.1.0',
    'description': '',
    'long_description': '# README\n\nParse and slice hadoop logs\n\n##\xa0Related\n\n- https://github.com/etsy/logster\n',
    'author': 'Khalid',
    'author_email': 'khalidck@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
