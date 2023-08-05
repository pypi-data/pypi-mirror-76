# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_optional_cython']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

extras_require = \
{'fast': ['cython>=0.29,<0.30']}

entry_points = \
{'console_scripts': ['pocy = poetry_optional_cython.cli:cli']}

setup_kwargs = {
    'name': 'poetry-optional-cython',
    'version': '0.0.3',
    'description': 'Package to demonstrate optional cython extension modules',
    'long_description': '# Poetry with optional Cython extension\n\nThis is a python packaging example project.\n\n## Installation\nInstall this package as pure python with `pip install poetry-optional-cython`.\nInstall with cython extension `pip install poetry-optional-cython[fast]`.\n\n## Running\nTry running the installed command:\n\n```bash\n$ pocy\n### Running as compiled extension ###\nHello Poetry with optional cython extension\nCalculating fib(36)\n14930352\n```\n\nThe first line of the command output will indicate if the cython extension module\ncompilation succeeded during installation.\n\n\n',
    'author': 'Titusz Pan',
    'author_email': 'tp@py7.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
