# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['configprops']

package_data = \
{'': ['*']}

install_requires = \
['termcolor>=1.1.0,<2.0.0']

setup_kwargs = {
    'name': 'configprops',
    'version': '1.0.0',
    'description': 'A configuration base class to be extended with list of KEYS (same prefix) that could be overridden by environment variables.',
    'long_description': '# configprops\n\n## Introduction\n\nThis packages defines a set of KEYS (sharing prefix) as configuration keys. Allow overriding from environment variables.\n\n## Examples\n\nExamples follows soon.\n',
    'author': 'Xu Yijun',
    'author_email': 'xuyijun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tommyxu/configprops',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
