# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pheme', 'pheme.version']

package_data = \
{'': ['*']}

install_requires = \
['coreapi>=2.3.3,<3.0.0',
 'django>=3.1,<4.0',
 'djangorestframework-dataclasses>=0.6,<0.7',
 'djangorestframework>=3.11.1,<4.0.0',
 'pdfkit>=0.6.1,<0.7.0',
 'pylint-django>=2.3.0,<3.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'uritemplate>=3.0.1,<4.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'pheme',
    'version': '0.0.1a1',
    'description': 'report-generation-service',
    'long_description': '![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)\n\n# Pheme - Greenbone Static Report Generator <!-- omit in toc -->\n\n**pheme** is a service to create scan reports. It is maintained by [Greenbone Networks].\n\n[Pheme](https://en.wikipedia.org/wiki/Pheme) is the personification of fame and renown.\n\nOr in this case personification of a service to generate reports.\n\n## Table of Contents <!-- omit in toc -->\n\n- [Installation](#installation)\n  - [Requirements](#requirements)\n- [Development](#development)\n- [Maintainer](#maintainer)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Installation\n\n### Requirements\n\nPython 3.7 and later is supported.\n\n## Development\n\n**pheme** uses [poetry] for its own dependency management and build\nprocess.\n\nFirst install poetry via pip\n\n    python3 -m pip install --user poetry\n\nAfterwards run\n\n    poetry install\n\nin the checkout directory of **pheme** (the directory containing the\n`pyproject.toml` file) to install all dependencies including the packages only\nrequired for development.\n\nAfterwards activate the git hooks for auto-formatting and linting via\n[autohooks].\n\n    poetry run autohooks activate\n\nValidate the activated git hooks by running\n\n    poetry run autohooks check\n\n## API overview\n\nTo get an overview of the API you can start this project\n\n```\npython manage.py runserver\n```\n\nand then go to [swagger](http://localhost:8000/docs/)\n\n\n## Maintainer\n\nThis project is maintained by [Greenbone Networks GmbH][Greenbone Networks]\n\n## Contributing\n\nYour contributions are highly appreciated. Please\n[create a pull request](https://github.com/greenbone/pheme/pulls)\non GitHub. Bigger changes need to be discussed with the development team via the\n[issues section at GitHub](https://github.com/greenbone/pheme/issues)\nfirst.\n\n## License\n\nCopyright (C) 2020 [Greenbone Networks GmbH][Greenbone Networks]\n\nLicensed under the [GNU General Public License v3.0 or later](LICENSE).\n\n[Greenbone Networks]: https://www.greenbone.net/\n[poetry]: https://python-poetry.org/\n[autohooks]: https://github.com/greenbone/autohooks\n',
    'author': 'Greenbone Networks GmbH',
    'author_email': 'info@greenbone.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
