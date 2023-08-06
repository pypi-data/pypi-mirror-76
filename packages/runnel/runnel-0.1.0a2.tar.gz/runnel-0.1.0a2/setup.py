# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['runnel', 'runnel.middleware']

package_data = \
{'': ['*'], 'runnel': ['lua/*']}

install_requires = \
['aiostream>=0.4.1,<0.5.0',
 'anyio>=2.0.0-beta.1,<3.0.0',
 'aredis>=1.1.8,<2.0.0',
 'colorama>=0.4.3,<0.5.0',
 'croniter>=0.3.34,<0.4.0',
 'hiredis>=1.0.1,<2.0.0',
 'pydantic>=1.5.1,<2.0.0',
 'pytz>=2020.1,<2021.0',
 'structlog>=20.1.0,<21.0.0',
 'typer>=0.3.0,<0.4.0']

extras_require = \
{'fast': ['uvloop>=0.14.0,<0.15.0',
          'xxhash>=1.4.4,<2.0.0',
          'orjson>=3.2.1,<4.0.0',
          'lz4>=3.1.0,<4.0.0']}

entry_points = \
{'console_scripts': ['runnel = runnel.cli:cli']}

setup_kwargs = {
    'name': 'runnel',
    'version': '0.1.0a2',
    'description': 'Distributed event processing for Python based on Redis Streams',
    'long_description': None,
    'author': 'Matt Westcott',
    'author_email': 'm.westcott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
