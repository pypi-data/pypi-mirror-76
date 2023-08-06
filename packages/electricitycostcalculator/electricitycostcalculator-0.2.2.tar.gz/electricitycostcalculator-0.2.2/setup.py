# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['electricitycostcalculator',
 'electricitycostcalculator.cost_calculator',
 'electricitycostcalculator.oadr_signal',
 'electricitycostcalculator.openei_tariff']

package_data = \
{'': ['*']}

install_requires = \
['holidays>=0.9.10,<0.10.0',
 'lxml>=4.3,<5.0',
 'matplotlib>=3.0,<4.0',
 'pandas>=0.24.2,<0.25.0',
 'pytz>=2019.1,<2020.0',
 'requests>=2.21,<3.0']

setup_kwargs = {
    'name': 'electricitycostcalculator',
    'version': '0.2.2',
    'description': '',
    'long_description': None,
    'author': 'Olivier Van Cutsem',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
