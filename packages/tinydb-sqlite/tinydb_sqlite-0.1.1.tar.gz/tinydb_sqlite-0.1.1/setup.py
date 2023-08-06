# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinydb_sqlite']

package_data = \
{'': ['*']}

install_requires = \
['tinydb>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'tinydb-sqlite',
    'version': '0.1.1',
    'description': '',
    'long_description': "# tinydb_sqlite\n\n## Usage\n\n``` py\nfrom tinydb import TinyDb\nfrom tinydb_sqlite import SQLiteStorage\n\nwith TinyDB(storage=SQLiteStorage, connection='db.sqlite') as db:\n    ...\n```\n",
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
