# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onemap_py']

package_data = \
{'': ['*']}

install_requires = \
['pypolyline>=0.2.4,<0.3.0']

setup_kwargs = {
    'name': 'onemap-py',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'tauculator',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
