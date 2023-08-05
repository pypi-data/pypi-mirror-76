# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonny_common_sql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'lonny-common-sql',
    'version': '0.1.0',
    'description': 'A library for building inline SQL queries safely using python callables.',
    'long_description': '# `lonny_common_sql`\n\nA library for building inline SQL queries safely using python `callables`.\n\n## Installation:\n\n```bash\npip install lonny_common_sql\n```\n\n## Usage:\n\nUsage is very straightforward. Please see example below:\n\n```python\nfrom lonny_common_sql import build\n\ntable = "TABLE"\nvalue = "VALUE"\n\nsql, params = build(lambda w: f"""\n    SELECT * FROM {table}\n    WHERE value = {w(value)}\n""")\n```\n\nWe simply pass `build` a callable that takes a `wrapper` argument. This wrapper is itself a `callable` that returns the substituted parameter name whilst simultaneously adds the value to the parameter dictionary to be returned along with the finalized SQL.\n\n',
    'author': 'tlonny',
    'author_email': 't@lonny.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://lonny.io',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
