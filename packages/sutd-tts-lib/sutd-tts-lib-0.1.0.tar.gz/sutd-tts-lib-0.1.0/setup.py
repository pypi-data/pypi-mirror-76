# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sutd', 'sutd.tts']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'fake-headers>=1.0.2,<2.0.0',
 'poetry>=4.9.1,<5.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'sutd-tts-lib',
    'version': '0.1.0',
    'description': "A (relatively) lightweight library for programmatically submitting entries to SUTD's Temperature Taking System, without Selenium and the like.",
    'long_description': None,
    'author': 'Chester',
    'author_email': 'chester8991@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
