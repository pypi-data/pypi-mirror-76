# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['text_template']

package_data = \
{'': ['*']}

install_requires = \
['ansi-colours==0.2.3',
 'codecov==2.0.15',
 'coverage==4.5.1',
 'importlib_resources>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'text-template',
    'version': '1.0.1',
    'description': 'Very simple text templating view for Python',
    'long_description': None,
    'author': 'Sarcoma',
    'author_email': 'sarcoma@live.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
