# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['snregales', 'snregales.classes', 'snregales.classes.abstract']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx_rtd_theme>=0.5.0,<0.6.0', 'rstcheck>=3.3.1,<4.0.0'],
 'lint': ['flake8-isort==3.0.0', 'isort>=4.3.20,<5.0.0'],
 'local': ['pytest-tldr==0.2.1',
           'pytest-cov>=2.9.0,<3.0.0',
           'flake8-isort==3.0.0',
           'isort>=4.3.20,<5.0.0',
           'sphinx_rtd_theme>=0.5.0,<0.6.0',
           'rstcheck>=3.3.1,<4.0.0'],
 'test': ['pytest-cov>=2.9.0,<3.0.0']}

setup_kwargs = {
    'name': 'snregales',
    'version': '0.1.0',
    'description': 'snregales python libraries',
    'long_description': None,
    'author': 'Sharlon Regales',
    'author_email': 'sharlonregales+dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
