# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elt_tools_aio', 'elt_tools_aio.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyMySQL', 'psycopg2', 'pybigquery', 'sqlalchemy-aio', 'sqlalchemy-redshift']

entry_points = \
{'console_scripts': ['run = main:main']}

setup_kwargs = {
    'name': 'elt-tools-aio',
    'version': '0.1.0',
    'description': 'Tools for monitoring and troubleshooting ELT arrangements.',
    'long_description': '# ELT-Tools-AIO\n![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&colorB=a3be8c)\n[![GitHub Issues](https://img.shields.io/github/issues/dewaldabrie/elt_tools_aio.svg?style=flat-square&colorA=4c566a&colorB=ebcb8b)](https://github.com/dewaldabrie/elt_tools_aio/issues)\n[![GitHub Stars](https://img.shields.io/github/stars/dewaldabrie/elt_tools_aio.svg?style=flat-square&colorB=ebcb8b&colorA=4c566a)](https://github.com/dewaldabrie/elt_tools_aio/stargazers)\n[![GitHub Forks](https://img.shields.io/github/forks/dewaldabrie/elt_tools_aio.svg?style=flat-square&colorA=4c566a&colorB=ebcb8b)](https://github.com/dewaldabrie/elt_tools_aio/network)\n\n## Database Abstraction\n\nA set of tools to serve as an abstraction layer over many commonly used databases, as long\nas it\'s supported by SQLAlchemy. It supports the following operations in an easy-to-use \ninterface:\n\n* asynchronous (non-blocking) operation\n* count the number of rows in a table\n* find duplicates in a table\n* find records missing in target with respect to source\n* find records on target which have been hard deleted from source\n* execute a sql query against a table\n\n## ELT Pair Operations\n\nIn Extract-Load-Transform (ELT) operations, a table is extracted and loaded from one database\nto another with potential transformations after that (for example in a database view). This is\nakin to database replication, albeit not necessarily all tables nor all columns are transferred. \nOne may also only transfer records from a certain date onwards. \n\n[comment]: <> ( ![alt text]\\(images/source-target-venn.svg?raw=true\\) )\n<img src="images/source-target-venn.svg" alt="source-target-records-venn" width="400" height="400">\n\nMany common database engineering tasks relate to the source and target pairs. This library \nassists by implementing these commonly performed operations in a succinct interface such as:\n\n* show a list of common tables between source and target database\n* compare counts between source and target tables over a specified time window\n* find primary keys of missing records in the target\n* fill missing records into the target over a given date range\n* find primary keys of orphaned records in the target (i.e. corresponding records from the \n  source database have been deleted)\n* remove orphaned records from target (even for large tables)\n\n## Configuration and Examples\nThe library provides two main classes: `DataClient` for database abstraction and `ELTDBPair` for \nELT operations between database pairs. The user passes configuration dictionaries into these classes.\nThe configuration describes database credentials, and details of which databases to pair up. \n\nFor example, to find duplicate on a particular table:\n\n```python\nimport asyncio\nfrom os import environ\nfrom elt_tools_aio.client import DataClientFactory\n\nDATABASES = {\n    \'db_key11\': {\n        \'engine\': \'oltp_engine\',\n        \'sql_alchemy_conn_string\': environ.get(\'mysql_db_uri\'),\n    },\n    \'db_key12\': {\n        \'engine\': \'bigquery_engine\',\n        \'dataset_id\': \'mydata\',\n        \'gcp_project\': environ.get(\'GCP_PROJECT\'),\n        \'gcp_credentials\': environ.get(\'GOOGLE_APPLICATION_CREDENTIALS\'),\n    },\n}\n\nasync def print_duplicate_keys():\n    factory = DataClientFactory(DATABASES)\n    client = factory(db_key=\'db_key11\')\n    customer_duplicates = await client.find_duplicate_keys(\'customers\', \'id\')\n    print(customer_duplicates)\n\n\nasyncio.run(print_duplicate_keys())\n```\n\nFor example, to remove orphaned records on the target table of a particular ELT Pair\nusing a binary search strategy on a large table:\n\n```python\nimport asyncio\nfrom os import environ\nfrom elt_tools_aio.client import ELTDBPairFactory\n\nDATABASES = {\n    \'db_key11\': {\n        \'engine\': \'oltp_engine\',\n        \'sql_alchemy_conn_string\': environ.get(\'mysql_db_uri\'),\n    },\n    \'db_key12\': {\n        \'engine\': \'bigquery_engine\',\n        \'dataset_id\': \'mydata\',\n        \'gcp_project\': environ.get(\'GCP_PROJECT\'),\n        \'gcp_credentials\': environ.get(\'GOOGLE_APPLICATION_CREDENTIALS\'),\n    },\n}\nELT_PAIRS = {\n    \'pair1\': {\n        \'source\': \'db_key11\', \'target\': \'db_key12\'\n    },\n}\n\nasync def remove_orphans():\n    factory = ELTDBPairFactory(ELT_PAIRS, DATABASES)\n    elt_pair = factory(pair_key=\'pair1\')\n    _ = await elt_pair.remove_orphans_from_target_with_binary_search(\n        \'customers\', \n        \'id\', \n        timestamp_fields=[\'created_at\']\n    )\n\nasyncio.run(remove_orphans())\n```\n\n## Installation instructions\n\n```shell\n$ pip install git+ssh://git@github.com/dewaldabrie/elt_tools_aio.git\n```\n\n',
    'author': 'Dewald Abrie',
    'author_email': 'dewaldabrie@gmail.com',
    'maintainer': 'Dewald Abrie',
    'maintainer_email': 'dewaldabrie@gmail.com',
    'url': 'https://github.com/dewaldabrie/elt_tools_aio/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
