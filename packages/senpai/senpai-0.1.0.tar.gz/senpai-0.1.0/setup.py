# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['senpai']

package_data = \
{'': ['*']}

install_requires = \
['loguru', 'psutil']

setup_kwargs = {
    'name': 'senpai',
    'version': '0.1.0',
    'description': 'Notices you',
    'long_description': '# Senpai\n\nNotices you\n',
    'author': 'sangarshanan',
    'author_email': 'sangarshanan1998@gmail.com',
    'maintainer': 'sangarshanan',
    'maintainer_email': 'sangarshanan1998@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
