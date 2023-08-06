# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_doh']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0', 'async_dns>=1.0.11,<2.0.0']

setup_kwargs = {
    'name': 'async-doh',
    'version': '0.1.0',
    'description': 'DNS over HTTPS based on aiohttp and async_dns',
    'long_description': "# async-doh\n\n[![PyPI](https://img.shields.io/pypi/v/async-doh.svg)]()\n\nDNS over HTTPS based on aiohttp and [async_dns](https://github.com/gera2ld/async_dns).\n\n## Installation\n\n```sh\n$ pip install async-doh\n```\n\n## Usage\n\n### Client\n\n```py\nimport asyncio\nfrom async_doh.client import query\n\nasync def main():\n    result = await query('https://1.1.1.1/dns-query', 'www.google.com', 'A')\n    print('query:', result)\n    result = await query_json('https://1.1.1.1/dns-query', 'www.google.com', 'A')\n    print('query_json:', result)\n\nasyncio.run(main())\n```\n\n### Server\n\n```py\nfrom aiohttp import web\nfrom async_doh.server import application\n\nweb.run(application)\n```\n\nNow you have `http://localhost:8080/dns-query` as an endpoint.\n",
    'author': 'Gerald',
    'author_email': 'gera2ld@live.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gera2ld/async-doh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
