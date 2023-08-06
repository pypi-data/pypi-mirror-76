# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['xbrief',
 'xbrief.bracket',
 'xbrief.deco',
 'xbrief.deco.deco_entries',
 'xbrief.deco.deco_json',
 'xbrief.deco.deco_matrix',
 'xbrief.deco.deco_str',
 'xbrief.deco.deco_vector',
 'xbrief.enum',
 'xbrief.enum.brackets',
 'xbrief.formatter',
 'xbrief.lines',
 'xbrief.logger',
 'xbrief.margin',
 'xbrief.margin.entries_margin',
 'xbrief.margin.matrix_margin',
 'xbrief.margin.utils',
 'xbrief.margin.vector_margin',
 'xbrief.padder',
 'xbrief.padder.pad_entries',
 'xbrief.padder.pad_keyed_column',
 'xbrief.padder.pad_matrix',
 'xbrief.padder.pad_string',
 'xbrief.padder.pad_table',
 'xbrief.padder.pad_vector']

package_data = \
{'': ['*']}

install_requires = \
['aryth>=0.0.5',
 'intype>=0.0.2',
 'ject>=0.0.1',
 'palett>=0.0.4',
 'texting>=0.0.3',
 'veho>=0.0.4']

setup_kwargs = {
    'name': 'xbrief',
    'version': '0.0.5',
    'description': 'pretty print',
    'long_description': None,
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
