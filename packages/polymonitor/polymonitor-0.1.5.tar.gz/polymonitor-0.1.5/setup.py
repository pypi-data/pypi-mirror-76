# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polymonitor']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'validators>=0.17.1,<0.18.0']

entry_points = \
{'console_scripts': ['polymonitor = polymonitor.cli:main']}

setup_kwargs = {
    'name': 'polymonitor',
    'version': '0.1.5',
    'description': 'Polymonitor can be used as a stand alone CLI tool to quickly check the status of a URL or as a plugin for polybar.',
    'long_description': '# Polymonitor\n\nPolymonitor can be used as a stand alone CLI tool to quickly check the status of a URL or as a plugin for [polybar](https://github.com/polybar/polybar).\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install polymonitor.\n\n```bash\n$ pip install polymonitor\n```\n\nAlternatively you can clone the git repository and use [Poetry](https://python-poetry.org/docs/) to install it.\n```bash\n$ git clone https://github.com/hegelocampus/polymonitor\n$ cd polymonitor\n$ poetry install\n```\n\n## Usage\n```bash\npolymonitor --help \nusage: Displays site status for polybar. [-h] [-s] [-c] [-u URLS [URLS ...]]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s, --symbolic        Displays the results as symbols\n  -c, --compact         Reduces the results into a more compact package\n  -u URLS [URLS ...], --urls URLS [URLS ...]\n                        Pass in URLs to monitor\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Bee',
    'author_email': 'bellis8099@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hegelocampus/polymonitor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
