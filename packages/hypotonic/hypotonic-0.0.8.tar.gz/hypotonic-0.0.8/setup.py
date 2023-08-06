# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypotonic']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.0.9', 'cssselect>=1.0.3', 'lxml>=4.1.1', 'parsel>=1.2.0']

setup_kwargs = {
    'name': 'hypotonic',
    'version': '0.0.8',
    'description': 'Fast asynchronous web scraper with minimalist API.',
    'long_description': "# Hypotonic\n\nFast asynchronous web scraper with minimalist API inspired by awesome [node-osmosis](https://github.com/rchipka/node-osmosis).\n\nHypotonic provides SQLAlchemy-like command chaining DSL to define HTML scrapers. Everything is executed asynchronously via `asyncio` and is ultra-fast thanks to `lxml` parser. Supports querying by XPath or CSS selectors.\n\nHypotonic does not natively execute JavaScript on websites and it is recommended to use [prerender](https://prerender.com).\n\n## Installing\n\nHypotonic requires Python 3.6+ and `libxml2` C library.\n\n`pip install hypotonic`\n\n## Example\n\n```python\nfrom hypotonic import Hypotonic\n\ndata, errors = (\n  Hypotonic()\n    .get('http://books.toscrape.com/')\n    .paginate('.next a::attr(href)', 5)\n    .find('.product_pod h3')\n    .set('title')\n    .follow('a::attr(href)')\n    .set({'price': '.price_color',\n          'availability': 'p.availability'})\n    .data()\n)\n```\n",
    'author': 'Martin Scavnicky',
    'author_email': 'martin.scavnicky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mscavnicky/hypotonic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
