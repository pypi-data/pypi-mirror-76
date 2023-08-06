# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saturn_notebook']

package_data = \
{'': ['*']}

install_requires = \
['argh>=0.26.2,<0.27.0',
 'atomicwrites>=1.4.0,<2.0.0',
 'dill>=0.3.2,<0.4.0',
 'importlib_metadata>=1.7.0,<2.0.0',
 'markdown>=3.2.2,<4.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'more_itertools>=8.4.0,<9.0.0',
 'ptpython>=3.0.2,<4.0.0',
 'pygments>=2.6.1,<3.0.0',
 'rich>=2.2.3,<3.0.0',
 'wurlitzer>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['saturn = saturn_notebook.__main__:main']}

setup_kwargs = {
    'name': 'saturn-notebook',
    'version': '1.0.0',
    'description': 'Plain-text Python notebooks with checkpointing',
    'long_description': None,
    'author': 'Dmitriy Morozov',
    'author_email': 'dmitriy@mrzv.org',
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
