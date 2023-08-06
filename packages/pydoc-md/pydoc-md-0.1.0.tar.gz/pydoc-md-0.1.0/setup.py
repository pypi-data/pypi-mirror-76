# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydoc_md']

package_data = \
{'': ['*']}

install_requires = \
['docstring_parser>=0.7.2,<0.8.0', 'fire>=0.3.1,<0.4.0', 'loguru>=0.5.1,<0.6.0']

entry_points = \
{'console_scripts': ['pydoc-md = pydoc_md.__main__:main']}

setup_kwargs = {
    'name': 'pydoc-md',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
