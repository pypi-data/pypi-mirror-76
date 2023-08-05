# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ez_sendgrid']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.2.1,<0.3.0',
 'python-decouple>=3.1,<4.0',
 'pyyaml>=5.1.2,<6.0.0',
 'sendgrid>=6.0.5,<7.0.0']

entry_points = \
{'console_scripts': ['ez-sendgrid = ez_sendgrid.cmd:main']}

setup_kwargs = {
    'name': 'ez-sendgrid',
    'version': '1.1.0',
    'description': 'Manage your SendGrid templates easy.',
    'long_description': None,
    'author': 'Alex Khaerov',
    'author_email': 'i@hayorov.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
