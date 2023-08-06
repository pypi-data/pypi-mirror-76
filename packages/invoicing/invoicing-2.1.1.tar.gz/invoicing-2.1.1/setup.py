# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invoicing',
 'invoicing.actions',
 'invoicing.api',
 'invoicing.constants',
 'invoicing.controller',
 'invoicing.crud',
 'invoicing.database',
 'invoicing.latex',
 'invoicing.model_validation',
 'invoicing.models',
 'invoicing.query_builder',
 'invoicing.relationships',
 'invoicing.repository',
 'invoicing.transformer',
 'invoicing.ui',
 'invoicing.value_validation']

package_data = \
{'': ['*'],
 'invoicing': ['sqlite/invoicing_bk.db',
               'sqlite/invoicing_bk.db',
               'sqlite/invoicing_bk.db',
               'sqlite/invoicing_dev.db',
               'sqlite/invoicing_dev.db',
               'sqlite/invoicing_dev.db',
               'sqlite/invoicing_local.db',
               'sqlite/invoicing_local.db',
               'sqlite/invoicing_local.db',
               'templates/*']}

install_requires = \
['Flask==1.0.2',
 'Jinja2==2.10.3',
 'Pygments==2.2.0',
 'Werkzeug==0.16.0',
 'ansi-colours==0.2.6',
 'more-itertools==4.3.0',
 'pytest==3.10.0',
 'python-dateutil==2.7.5',
 'python-dotenv==0.9.1',
 'text-template==0.1.4',
 'uWSGI==2.0.17.1',
 'unicode==2.6']

entry_points = \
{'console_scripts': ['invoicing = invoicing.__main__:main']}

setup_kwargs = {
    'name': 'invoicing',
    'version': '2.1.1',
    'description': 'Generate invoice PDF from LaTeX template',
    'long_description': None,
    'author': 'Sarcoma',
    'author_email': 'sean@orderandchaoscreative.com',
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
