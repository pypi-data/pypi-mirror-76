# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['plz']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=3.0', 'colorama>=0.4,<0.5']

entry_points = \
{'console_scripts': ['plz = plz.main:main']}

setup_kwargs = {
    'name': 'plz-cmd',
    'version': '0.9.0',
    'description': 'command line app for running configurable shell commands',
    'long_description': "## plz-cmd\n\n[![Build Status](https://travis-ci.org/m3brown/plz.svg?branch=master)](https://travis-ci.org/m3brown/plz)\n[![Coverage Status](https://coveralls.io/repos/github/m3brown/plz/badge.svg?branch=master)](https://coveralls.io/github/m3brown/plz?branch=master)\n\nA shell command to execute standard/repeatable commands in a git repo\n\n### Installation\n\nInstall plz at the system level so that it only has to be installed once.\n\n```bash\npip install plz-cmd\n\n# sudo may be required on your machine\nsudo pip install plz-cmd\n```\n\nIt can also be installed inside a virtualenv.  However, this means you'll have\nto install plz-cmd for each each virtualenv in use.\n\n```bash\nvirtualenv venv\n. venv/bin/activate\n\npip install plz-cmd\n```\n\n### Example\n\nplz looks for a `.plz.yaml` file either in the current directory or in the root\nof the git repo you're currently in. This file can (and should) be checked into\nversion control.\n\nFor a .plz.yaml file located in the git root directory, commands run will be\nexecuted relative to that directory, not the current directory.\n\nSuppose we have the following `.plz.yaml` file:\n\n```yaml\n- id: run\n  cmd: ./manage.py runserver\n- id: test\n  cmd:\n  - ./manage.py test\n  - yarn test\n- id: setup\n  cmd:\n  - poetry install\n  - poetry run ./manage.py migrate\n  - yarn install\n- id: ls\n  cmd: ls\n```\n\nThe following commands would be available:\n\n```bash\nplz run\nplz test\nplz setup\n```\n\n### Globbing\n\nplz supports asterisk expansion.  For example, the cmd `ls *.py` will work as expected.\n\n### Runtime arguments\n\nplz supports passing custom arguments when running the plz command. For example:\n\n```\n# bind to port 8001 instead of the default 8000\nplz run 127.0.0.1:8001\n```\n\nAny passed arguments will be tested to see if they are file paths relative to\nthe current directory when running the command. Using this repo as an example:\n\n```\nbash$ ls .*.yaml\n.plz.yaml               .pre-commit-config.yaml\n\nbash$ cd plz\n\nbash$ plz ls ../.*.yaml\n\n[INFO] Using config: /path/plz/.plz.yaml\n\n===============================================================================\nRunning command: ls\n===============================================================================\n\n.plz.yaml\n.pre-commit-config.yaml\n\n[INFO] Process complete, return code: 0\n\nbash$ plz ls __*.py\n\n[INFO] Using config: /path/plz/.plz.yaml\n\n===============================================================================\nRunning command: ls\n===============================================================================\n\nplz/__init__.py\n\n[INFO] Process complete, return code: 0\n```\n\n### Development\n\nSetting up for development is easy when plz is already installed!\n\n```\ngit clone https://github.com/m3brown/plz\ncd plz\nplz setup\nplz test\n```\n",
    'author': 'Mike Brown',
    'author_email': 'mike.brown@excella.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m3brown/plz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
