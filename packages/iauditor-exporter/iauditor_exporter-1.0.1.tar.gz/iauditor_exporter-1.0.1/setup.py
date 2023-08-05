# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'iauditor_exporter'}

packages = \
['modules']

package_data = \
{'': ['*']}

modules = \
['exporter', 'csvExporter']
install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'SQLAlchemy>=1.3.4',
 'coloredlogs>=10.0',
 'dateparser>=0.7.6,<0.8.0',
 'numpy>=1.16.4',
 'pandas>=0.24.2',
 'python_dateutil>=2.8.0',
 'pytz>=2019.2',
 'questionary>=1.5.2,<2.0.0',
 'rich>=4.2.2,<5.0.0',
 'safetyculture-sdk-python-beta>=2.1.1',
 'sqlalchemy-pyodbc-mssql>=0.1.0',
 'tqdm>=4.46.0,<5.0.0',
 'tzlocal>=2.0.0',
 'unicodecsv>=0.14.1']

entry_points = \
{'console_scripts': ['ia_exporter = exporter:main']}

setup_kwargs = {
    'name': 'iauditor-exporter',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'Edd',
    'author_email': 'edward.abrahamsen-mills@safetyculture.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
