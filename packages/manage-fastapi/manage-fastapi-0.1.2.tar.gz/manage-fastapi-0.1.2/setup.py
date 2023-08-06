# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manage_fastapi']

package_data = \
{'': ['*']}

install_requires = \
['databases[postgresql,sqlite]>=0.3.2,<0.4.0',
 'fastapi>=0.60.1,<0.61.0',
 'typer>=0.3.1,<0.4.0',
 'uvicorn>=0.11.8,<0.12.0']

entry_points = \
{'console_scripts': ['manage-fastapi = manage_fastapi.main:app']}

setup_kwargs = {
    'name': 'manage-fastapi',
    'version': '0.1.2',
    'description': 'Managing FastAPI projects made easy.',
    'long_description': '\n\n<h3 align="center">\n    <strong>Managing FastAPI projects made easy</strong>\n</h3>\n<p align="center">\n<img src="https://img.shields.io/github/issues/ycd/manage-fastapi?style=for-the-badge">\n<a href="https://github.com/ycd/manage-fastapi" target="_blank">\n    <img src="https://img.shields.io/bitbucket/pr-raw/ycd/manage-fastapi?style=for-the-badge" alt="Build">\n</a>\n<a href="https://github.com/ycd/manage-fastapi" target="_blank">\n    <img src="https://img.shields.io/github/last-commit/ycd/manage-fastapi?style=for-the-badge" alt="Latest Commit">\n</a>\n<br />\n<a href="https://pypi.org/project/fastapi-utils" target="_blank">\n    <img src="https://img.shields.io/pypi/v/manage-fastapi?style=for-the-badge" alt="Package version">\n</a>\n    <img src="https://img.shields.io/pypi/pyversions/manage-fastapi?style=for-the-badge">\n    <img src="https://img.shields.io/github/license/ycd/manage-fastapi?style=for-the-badge">\n</p>\n\n\n---\n\n**Documentation**: View it on [website](https://ycd.github.io/manage-fastapi/)\n\n**Source Code**: View it on [Github](https://github.com/ycd/manage-fastapi/)\n\n\n---\n\n\n\n##  Features :rocket:\n\n* #### Creates customizable **project boilerplate.**\n* #### Creates customizable **app boilerplate.**\n* #### More will come soon.\n\n\n## Example folder structure for more check [documentation](https://ycd.github.io/manage-fastapi/)\n```\nnewproject/\n├── __init__.py\n├── main.py\n├── newproject\n│\xa0\xa0 ├── models\n│\xa0\xa0 │\xa0\xa0 ├── database.py\n│\xa0\xa0 │\xa0\xa0 └── __init__.py\n│\xa0\xa0 ├── schemas\n│\xa0\xa0 │\xa0\xa0 ├── __init__.py\n│\xa0\xa0 │\xa0\xa0 └── schema.py\n│\xa0\xa0 └── settings.py\n├── tests\n│\xa0\xa0 ├── __init__.py\n│\xa0\xa0 └── v1\n│\xa0\xa0     ├── __init__.py\n│\xa0\xa0     └── test_v1.py\n└── v1\n    ├── api.py\n    ├── endpoints\n    │\xa0\xa0 ├── endpoint.py\n    │\xa0\xa0 └── __init__.py\n    └── __init__.py\n```\n\n## Installation :pushpin:\n\n`pip install manage-fastapi`\n\n\n## Release Notes :mega:\n\n### Latest Changes\n\n### 0.1.2\n\n* Add tests\n* Fix and relocate success message \n* Add travis \n\n### 0.1.1\n\n* Added documentation\n* Fixed typos\n* Additional response for successfuly creation.\n\n### 0.1.0\n\n* Prototype of project with two functionalities.\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'ycd',
    'author_email': 'yagizcanilbey1903@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ycd/manage-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
