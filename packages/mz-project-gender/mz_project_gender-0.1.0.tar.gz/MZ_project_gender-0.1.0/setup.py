# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mz_project_gender', 'mz_project_gender.models']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'mz-project-gender',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mike',
    'author_email': 'mikezhang1970@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
