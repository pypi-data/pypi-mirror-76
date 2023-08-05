# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ariadne_utils',
 'ariadne_utils.cli',
 'ariadne_utils.directives',
 'ariadne_utils.directives.utils',
 'ariadne_utils.django',
 'ariadne_utils.scalars']

package_data = \
{'': ['*']}

install_requires = \
['ariadne>=0.12.0,<0.13.0',
 'click>=7.1.2,<8.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytimeparse>=1.1.8,<2.0.0',
 'validator-collection>=1.4.2,<2.0.0']

extras_require = \
{'django': ['django>=2.2,<3.0', 'channels>=2.4,<3.0']}

entry_points = \
{'console_scripts': ['ariadne-utils = ariadne_utils.cli:cli']}

setup_kwargs = {
    'name': 'ariadne-utils',
    'version': '0.1.2',
    'description': '',
    'long_description': '[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)\n[![PyPI version fury.io](https://badge.fury.io/py/ariadne-utils.svg)](https://pypi.org/project/ariadne-utils/)\n\n# ariadne-utils\n\nUtilities for using ariadne in Django, FastAPI, or other projects\n\n## Installation\n\n```shell script\n$ pip install ariadne-utils --upgrade\n```\n[Official PyPi Repository](https://pypi.org/project/ariadne-utils/)',
    'author': 'Marc Ford',
    'author_email': 'mrfxyz567@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mfdeux/ariadne-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
