# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioswitchbotmeter']

package_data = \
{'': ['*']}

install_requires = \
['bluepy>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'aioswitchbotmeter',
    'version': '0.1.1',
    'description': 'AsyncIO-compatible SwitchBot Meter library',
    'long_description': None,
    'author': 'David Francos',
    'author_email': 'opensource@davidfrancos.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
