# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arxiv_connections']

package_data = \
{'': ['*']}

install_requires = \
['arxiv>=0.5.3,<0.6.0',
 'click>=7.1.2,<8.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'nb_black>=1.0.7,<2.0.0',
 'networkx>=2.4,<3.0',
 'pandas>=1.1.0,<2.0.0',
 'plotly>=4.9.0,<5.0.0',
 'wheel>=0.34.2,<0.35.0']

entry_points = \
{'console_scripts': ['arxiv-connector = arxiv_connections.cli:main']}

setup_kwargs = {
    'name': 'arxiv-connections',
    'version': '0.1.1',
    'description': 'python package used to visualize academics and find related people',
    'long_description': None,
    'author': 'Roy Rinberg',
    'author_email': 'royrinberg@gmail.com',
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
