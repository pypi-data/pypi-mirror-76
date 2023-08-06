# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cihai', 'cihai.data', 'cihai.data.decomp', 'cihai.data.unihan']

package_data = \
{'': ['*']}

install_requires = \
['appdirs', 'click>=7', 'kaptan', 'sqlalchemy', 'unihan-etl>=0.11.0,<0.12.0']

extras_require = \
{'cli': ['cihai-cli']}

setup_kwargs = {
    'name': 'cihai',
    'version': '0.10.0',
    'description': 'Library for CJK (chinese, japanese, korean) language data.',
    'long_description': None,
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://cihai.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
