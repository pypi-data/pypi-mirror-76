# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitslice']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bitslice',
    'version': '0.2.0',
    'description': 'Verilog-like bitvector slicing',
    'long_description': None,
    'author': 'Zeger Van de Vannet',
    'author_email': 'zegervdv@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zegervdv/bitslice',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
