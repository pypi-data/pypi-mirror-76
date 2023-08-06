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
    'version': '0.4.7',
    'description': 'Git wrapper that offers more user friendly commands',
    'long_description': "# Gitutor\n\nWelcome to Gitutor. This tool is meant to get you up and running using git\nin the shortest time possible while learning on the go.\n\nGitutor is a command line application that wraps git and provides beginner \nfriendly versions of git's commands. It makes git easy. \n\nIn this tutorial you'll learn how tu use git with the aid of gitutor. Once \nyou feel comfortable using git this way, read what is going on behind gitutor's\ncommands on the last chapters.\n\nThe command line includes a summarized version of this tutorial so you'll always\nhave it at hand. To access it run: \n\n    $ gt lesson \n\nWhenever you execute a comand read it's output, it has useful information.\n\n## Available commands\n\n1. gt init - Initialize your local and remote repository.\n2. gt save - Save you changes in the local and remote repository.\n3. gt goback - Return to a previous commit.\n4. gt compare - Compare the current state with a previous commit.\n5. gt ignore - Make git ignore selected files.\n\n## Installation guide\n\nIn order to use gitutor without any dependencies version conflicts we recommend installing it using pipx.\n\nPipx creates a virtual environment for your package and exposes its entry point so you can run gitutor from anywhere. Install pipx and make sure the $PATH is correctly configured\n\n    $ python3 -m pip install --user pipx\n    $ pipx ensurepath\n\nOnce pipx is installed, run the following to install gitutor\n\n    $ pipx install gitutor\n\nAnd to upgrade gitutor to its latest version you only need to run\n\n    $ pipx upgrade gitutor\n\n## Additional notes\n\nBefore using gitutor you need to have git available in your computer. You can check the installation guide [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).\n\nIt's also recommended to store your GitHub credentials so you won't have to authenticate everytime you realize a push or pull. You can do this by running\n\n    $ git config --global credential.helper store\n\nThis will store your credentials in a plain-text file (.git-gredentials) under your project directory. If you don't like this you can use any of the following approaches:\n\nOn Mac OS X you can use its native keystore with\n\n    $ git config --global credential.helper oskeychain\n\nFor Windows you can install a helper called [Git Credential Manager for Windows](https://github.com/Microsoft/Git-Credential-Manager-for-Windows) and then run\n\n    $ git config --global credential.helper manager",
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
