# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wccls']

package_data = \
{'': ['*']}

install_requires = \
['pytest-vcr>=1.0.2,<2.0.0', 'requests-html>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'wccls',
    'version': '2.0.0',
    'description': 'Scraper for the WCCLS account page',
    'long_description': '# Overview\n\nThis is a scraper for the WCCLS account page.\n\n# Usage\n\n![image](https://github.com/rkhwaja/wccls/workflows/ci/badge.svg)\n\n``` python\nwccls = Wccls(login=cardNumber, password=password)\nfor item in wccls.items:\n    print(item)\n```\n',
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rkhwaja/wccls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
