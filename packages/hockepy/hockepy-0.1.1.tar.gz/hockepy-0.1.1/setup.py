# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hockepy', 'hockepy.commands']

package_data = \
{'': ['*']}

modules = \
['hocke']
install_requires = \
['requests>=2.24.0,<3.0.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['hockepy = hocke:run_hockepy']}

setup_kwargs = {
    'name': 'hockepy',
    'version': '0.1.1',
    'description': 'CLI utility and (a subset of) NHL API for hockey nerds',
    'long_description': '     ____  ____    ____      ______  ___  ____   _________  ______    ____  ____\n    |_   ||   _| .\'    `.  .\' ___  ||_  ||_  _| |_   ___  ||_   __ \\ |_  _||_  _|\n      | |__| |  /  .--.  \\/ .\'   \\_|  | |_/ /     | |_  \\_|  | |__) |  \\ \\  / /\n      |  __  |  | |    | || |         |  __\'.     |  _|  _   |  ___/    \\ \\/ /\n     _| |  | |_ \\  `--\'  /\\ `.___.\'\\ _| |  \\ \\_  _| |___/ | _| |_       _|  |_\n    |____||____| `.____.\'  `._____.\'|____||____||_________||_____|     |______|\n\n_(pronounced like hockey-py so probably something like_ /ˈhɑː.kipaɪ/_)_\n\n[![Build Status](https://travis-ci.com/geckon/hockepy.svg?branch=master)](https://travis-ci.com/geckon/hockepy)\n[![Codacy Badge](https://api.codacy.com/project/badge/Grade/88be5e28d236447b892bd9e6525bbff8)](https://app.codacy.com/app/geckon/hockepy?utm_source=github.com&utm_medium=referral&utm_content=geckon/hockepy&utm_campaign=Badge_Grade_Dashboard)\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/geckon/hockepy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/geckon/hockepy/alerts/)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/geckon/hockepy.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/geckon/hockepy/context:python)\n[![Updates](https://pyup.io/repos/github/geckon/hockepy/shield.svg)](https://pyup.io/repos/github/geckon/hockepy/)\n\n**Important:** Please keep in mind that `hockepy` is under active development\nand any part can be changed anytime.\n\n## Installation\n\n```\npip install hockepy\n```\n\n## CLI utility\n\nThe main purpose of `hockepy` is to provide a command line utility for geeky\nhockey fans. The easiest way to discover the features currently implemented is\nto display help:\n\n      $ hockepy -h\n    usage: hocke.py [-h] [-D] [-v] {today,schedule} ...\n\n    positional arguments:\n      {today,schedule}\n\n    optional arguments:\n      -h, --help        show this help message and exit\n      -D, --debug       turn debug output on\n      -v, --verbose     turn verbose output on\n\nSubcommands also support `-h` option:\n\n    $ hockepy schedule -h\n    usage: hocke.py schedule [-h] [--home-first] [--utc]\n                               [first_date] [last_date]\n\n    positional arguments:\n      first_date    first date to get schedule for\n      last_date     last date to get schedule for\n\n    optional arguments:\n      -h, --help    show this help message and exit\n      --home-first  print the home team first\n      --utc         print times in UTC instead of local time\n\nBear in mind that the actual help may differ as this listing won\'t necessarily\nbe updated with any feature addition/change.\n\n### Configuration\n\nYou can highlight your favorite team using a configuration file called\n`.hockepy.conf` (an example is included in the repository):\n\n```\nhighlight_teams = [\n    "Boston Bruins",\n    "Pittsburgh Penguins",\n]\n```\n\nThe file can be placed in the current working directory, your home directory or\nin a directory specified by HOCKEPY_CONF_DIR (hockepy checks in that order).\n\n## NHL API\n\nAnother goal is to offer a Python interface to a subset of NHL API. Other\nleagues may or may not be added as well but the main plan is to support NHL for\nnow.\n\nNHL API is available at <https://statsapi.web.nhl.com/api/v1/>. I am not aware\nof any available documentation so it\'s been discovering and trial-and-error for\nme so far. If you know about any documentation, let me know.\n\nPlease note that any usage of the API (and therefore usage of `hockepy` as\nwell) is likely subject to\n[NHL Terms of Service](https://www.nhl.com/info/terms-of-service).\n',
    'author': 'Tomáš Heger',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/geckon/hockepy',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
