# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ospd', 'ospd.command', 'tests', 'tests.command']

package_data = \
{'': ['*']}

modules = \
['COPYING', 'CHANGELOG', 'poetry', 'setup']
install_requires = \
['defusedxml>=0.6.0,<0.7.0',
 'deprecated>=1.2.10,<2.0.0',
 'lxml>=4.5.1,<5.0.0',
 'paramiko>=2.7.1,<3.0.0',
 'psutil>=5.7.0,<6.0.0']

setup_kwargs = {
    'name': 'ospd',
    'version': '20.8.0',
    'description': 'OSPD is a base for scanner wrappers which share the same\ncommunication protocol: OSP (Open Scanner Protocol)',
    'long_description': '![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)\n\n# ospd <!-- omit in toc -->\n\n[![GitHub releases](https://img.shields.io/github/release/greenbone/ospd.svg)](https://github.com/greenbone/ospd/releases)\n[![PyPI](https://img.shields.io/pypi/v/ospd.svg)](https://pypi.org/project/ospd/)\n[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/greenbone/ospd/badges/quality-score.png?b=ospd-20.08)](https://scrutinizer-ci.com/g/greenbone/ospd/?branch=ospd-20.08)\n[![code test coverage](https://codecov.io/gh/greenbone/ospd/branch/ospd-20.08/graphs/badge.svg)](https://codecov.io/gh/greenbone/ospd)\n[![CircleCI](https://circleci.com/gh/greenbone/ospd/tree/ospd-20.08.svg?style=svg)](https://circleci.com/gh/greenbone/ospd/tree/ospd-20.08)\n\nospd is a base class for scanner wrappers which share the same communication\nprotocol: OSP (Open Scanner Protocol). OSP creates a unified interface for\ndifferent security scanners and makes their control flow and scan results\nconsistently available under the central Greenbone Vulnerability Manager service.\n\nOSP is similar in many ways to GMP (Greenbone Management Protocol): XML-based,\nstateless and non-permanent connection.\n\nThe design supports wrapping arbitrary scanners with same protocol OSP,\nsharing the core daemon options while adding scanner specific parameters and\noptions.\n\n## Table of Contents\n\n- [Table of Contents](#table-of-contents)\n- [Releases](#releases)\n- [Installation](#installation)\n  - [Requirements](#requirements)\n  - [Install using pip](#install-using-pip)\n- [How to write your own OSP Scanner Wrapper](#how-to-write-your-own-osp-scanner-wrapper)\n- [Support](#support)\n- [Maintainer](#maintainer)\n- [Contributing](#contributing)\n- [License](#license)\n\n## Releases\n￼\nAll [release files](https://github.com/greenbone/ospd/releases) are signed with\nthe [Greenbone Community Feed integrity key](https://community.greenbone.net/t/gcf-managing-the-digital-signatures/101).\nThis gpg key can be downloaded at https://www.greenbone.net/GBCommunitySigningKey.asc\nand the fingerprint is `8AE4 BE42 9B60 A59B 311C  2E73 9823 FAA6 0ED1 E580`.\n\n## Installation\n\n### Requirements\n\nospd requires Python >= 3.5 along with the following libraries:\n\n    - python3-paramiko\n\n    - python3-lxml\n\n    - python3-defusedxml\n\n### Install using pip\n\nYou can install ospd from the Python Package Index using [pip](https://pip.pypa.io/):\n\n    python3 -m pip install ospd\n\nAlternatively download or clone this repository and install the latest development version:\n\n    python3 -m pip install .\n\n## How to write your own OSP Scanner Wrapper\n\nAs a core you need to derive from the class OSPDaemon from ospd.py.\nSee the documentation there for the single steps to establish the\nfull wrapper.\n\nSee the file [doc/INSTALL-ospd-scanner.md](doc/INSTALL-ospd-scanner.md) about how to register a OSP scanner at\nthe Greenbone Vulnerability Manager which will automatically establish a full\nGUI integration for the Greenbone Security Assistant (GSA).\n\nThere are some online resources about this topic:\n<https://docs.greenbone.net/GSM-Manual/gos-3.1/en/osp.html#how-to-write-your-own-osp-wrapper>\n\n## Support\n\nFor any question on the usage of OSPD please use the [Greenbone Community Portal](https://community.greenbone.net/c/osp). If you found a problem with the software, please [create an issue](https://github.com/greenbone/ospd/issues) on GitHub.\n\n## Maintainer\n\nThis project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).\n\n## Contributing\n\nYour contributions are highly appreciated. Please [create a pull request](https://github.com/greenbone/ospd/pulls) on GitHub. For bigger changes, please discuss it first in the [issues](https://github.com/greenbone/ospd/issues).\n\nFor development you should use [poetry](https://python-poetry.org)\nto keep you python packages separated in different environments. First install\npoetry via pip\n\n    python3 -m pip install --user poetry\n\nAfterwards run\n\n    poetry install\n\nin the checkout directory of ospd (the directory containing the\n`pyproject.toml` file) to install all dependencies including the packages only\nrequired for development.\n\nThe ospd repository uses [autohooks](https://github.com/greenbone/autohooks)\nto apply linting and auto formatting via git hooks. Please ensure the git hooks\nare active.\n\n    poetry install\n    poetry run autohooks activate --force\n\n## License\n\nCopyright (C) 2009-2020 [Greenbone Networks GmbH](https://www.greenbone.net/)\n\nLicensed under the [GNU Affero General Public License v3.0 or later](COPYING).\n',
    'author': 'Greenbone Networks GmbH',
    'author_email': 'info@greenbone.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/greenbone/ospd',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
