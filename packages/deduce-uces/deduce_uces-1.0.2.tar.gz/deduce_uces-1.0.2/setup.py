# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deduce_uces',
 'deduce_uces.commands',
 'deduce_uces.extenders',
 'deduce_uces.matchers',
 'deduce_uces.mergers',
 'deduce_uces.output']

package_data = \
{'': ['*']}

install_requires = \
['gffutils>=0.10.1,<0.11.0',
 'mappy>=2.17,<3.0',
 'networkx>=2.4,<3.0',
 'tqdm>=4.48.2,<5.0.0']

entry_points = \
{'console_scripts': ['deduce = deduce_uces.__main__:main']}

setup_kwargs = {
    'name': 'deduce-uces',
    'version': '1.0.2',
    'description': 'DedUCE is a tool for efficiently finding ultra-conserved elements across multiple genomes.',
    'long_description': None,
    'author': 'Cadel Watson',
    'author_email': 'cadel@cadelwatson.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
