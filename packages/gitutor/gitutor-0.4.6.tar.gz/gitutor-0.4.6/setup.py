# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitutor',
 'gitutor.compare',
 'gitutor.goBack',
 'gitutor.ignore',
 'gitutor.init',
 'gitutor.lesson',
 'gitutor.save']

package_data = \
{'': ['*']}

install_requires = \
['GitPython==3.1.3',
 'click==7.1.2',
 'colorama==0.4.3',
 'gitdb==4.0.5',
 'pygithub==1.51',
 'pyinquirer==1.0.3',
 'requests>=2.20.0,<3.0.0',
 'smmap==3.0.4']

entry_points = \
{'console_scripts': ['gt = gitutor.cli:main']}

setup_kwargs = {
    'name': 'gitutor',
    'version': '0.4.6',
    'description': 'Git wrapper that offers more user friendly commands',
    'long_description': '# gitutor\n\nGitutor is a git wrapper cli tool designed to get you up and running using git in the shortest amount of time possible while learning on the go. \n\n## Available commands\n1. gt init - Initialize your local and remote repository.\n2. gt save - Save you changes in the local and remote repository.\n3. gt goback - Return to a previous commit.\n4. gt compare - Compare the current state with a previous commit.\n5. gt ignore - Make git ignore selected files.\n\n',
    'author': 'AMAI',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitutor.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
