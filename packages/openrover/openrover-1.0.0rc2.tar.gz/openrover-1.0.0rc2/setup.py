# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['openrover']
install_requires = \
['roverpro']

setup_kwargs = {
    'name': 'openrover',
    'version': '1.0.0rc2',
    'description': 'Please use the roverpro package instead',
    'long_description': '#  Open Rover\n\nThe robot formerly known as "Open Rover" is now "Rover Pro"!\n\nPlease update code and documentation to point to the python [`roverpro` package](https://pypi.org/project/roverpro/) instead of `openrover`.\n',
    'author': 'Dan Rose',
    'author_email': 'dan@digilabs.io',
    'maintainer': 'Dan Rose',
    'maintainer_email': 'dan@digilabs.io',
    'url': 'https://github.com/RoverRobotics/roverpro-python',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
