# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strongline']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.6.1,<2.0.0']

extras_require = \
{'django': ['channels>=2.4,<3.0']}

setup_kwargs = {
    'name': 'strongline',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
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
