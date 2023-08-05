# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_common_pg']

package_data = \
{'': ['*']}

install_requires = \
['lonny_common_sql>=0.1.0,<0.2.0', 'psycopg2-binary>=2.8.5,<3.0.0']

setup_kwargs = {
    'name': 'lonny-common-pg',
    'version': '0.1.0',
    'description': 'A quality-of-life wrapper for the psycopg2 connection object.',
    'long_description': "# `lonny_common_pg`\n\nA quality-of-life wrapper for the psycopg2 connection object.\n\n## Installation\n\n```bash\npip install lonny_common_pg\n```\n\n## Usage\n\nTo import the connection object, simply do:\n\n```python\nfrom lonny_common_pg import Connection\n```\n\n - The connection object constructor takes `host`, `port`, `dbname`, `user` and `password` kwargs.\n - The connection isn't initialized until a query is made or `init` is explicitly called.\n - The connection can be closed by using `close` - however it can be subsequently re-opened at anytime. When used in a `with` contextmanager context - the connection is closed when leaving the block.\n - The 3 methods for querying the database are: `execute`, `fetch_one` and `fetch_all`. All of these can either take a SQL string, or a callable (see the `lonny_sql` module for usage).\n - This connection wrapper uses `autocommit` mode and the `DictCursor` for returning results.\n\n ### Nested Transactions\n\nNested transactions are possible using this library. The outermost transaction uses a standard `TRANSACTION` construct. Inner transactions use a `SAVEPOINT` instead.\n\n```python\nconn = Connection(**kwargs)\nwith conn.transaction():\n    try:\n        do_something_else()\n        with conn.transaction():\n            do_something()\n    except:\n        pass\n```\n\n",
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lonny.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
