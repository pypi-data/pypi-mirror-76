# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mozci', 'mozci.util']

package_data = \
{'': ['*'], 'mozci': ['queries/*']}

install_requires = \
['adr>=0.19,<0.20', 'taskcluster_urls>=12.1,<14.0']

setup_kwargs = {
    'name': 'mozci',
    'version': '1.6.7',
    'description': '',
    'long_description': None,
    'author': 'Andrew Halberstadt',
    'author_email': 'ahal@mozilla.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
