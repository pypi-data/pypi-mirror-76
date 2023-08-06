# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hyperspace_rpc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hyperspace-rpc',
    'version': '0.0.1a3',
    'description': 'Raw RPC layer for Hyperspace',
    'long_description': '# hyperspace-rpc\n\n[![Build Status](https://drone.autonomic.zone/api/badges/hyperpy/hyperspace-rpc/status.svg)](https://drone.autonomic.zone/hyperpy/hyperspace-rpc)\n\n## Raw RPC layer for Hyperspace\n\n## Install\n\n```sh\n$ pip install hyperspace-rpc\n```\n\n## Example\n\nSee [hyperpy/hyperspace-client](https://github.com/hyperpy/hyperspace-client).\n',
    'author': 'decentral1se',
    'author_email': 'hi@decentral1.se',
    'maintainer': 'decentral1se',
    'maintainer_email': 'hi@decentral1.se',
    'url': 'https://github.com/hyperpy/hyperspace-rpc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
