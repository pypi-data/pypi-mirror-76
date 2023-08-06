# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tenhoulog']

package_data = \
{'': ['*']}

install_requires = \
['beautifultable>=1.0.0,<2.0.0',
 'httpx>=0.13.3,<0.14.0',
 'japanize-matplotlib>=1.1.2,<2.0.0',
 'matplotlib>=3.3.0,<4.0.0',
 'pandas>=1.1.0,<2.0.0',
 'pydantic>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'tenhoulog',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'kitagawa-hr',
    'author_email': 'kitagawa@cancerscan.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
