# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiktokpy',
 'tiktokpy.bot',
 'tiktokpy.cli',
 'tiktokpy.client',
 'tiktokpy.models',
 'tiktokpy.models.html',
 'tiktokpy.parsers',
 'tiktokpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.0.0,<4.0.0',
 'humanize>=2.5.0,<3.0.0',
 'loguru>=0.5.0,<0.6.0',
 'pydantic>=1.6.1,<2.0.0',
 'pyppeteer-stealth>=1.0.0,<2.0.0',
 'pyppeteer>=0.2.2,<0.3.0',
 'tqdm>=4.48.0,<5.0.0',
 'typer>=0.3.1,<0.4.0']

extras_require = \
{'html': ['parsel>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['tiktok_login = tiktokpy.cli:app']}

setup_kwargs = {
    'name': 'tiktokpy',
    'version': '0.7.2',
    'description': '',
    'long_description': None,
    'author': 'Evgeny Kemerov',
    'author_email': 'eskemerov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
