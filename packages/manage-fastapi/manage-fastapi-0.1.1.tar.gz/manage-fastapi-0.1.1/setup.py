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
    'version': '0.1.1',
    'description': 'Managing FastAPI projects made easy.',
    'long_description': '\n\n\n## Starting new FastAPI projects made easy.\n\n**manage-fastapi** is a command line tool to manage your FastAPI projects easily. \n\n\n###  Features :rocket:\n\n* Creates customizable **project boilerplate.**\n* Craetes customizable **app boilerplate.**\n\n\nHow to use it\n\n```python\nmanage-fastapi startproject [ARGS] \nmanage-fastapi startapp [ARGS]\n```\n\n\n## Release Notes :mega:\n\n### Latest Changes\n\n### 0.1.0\n\n* Prototype of project with two functionalities.\n\n## License\n\nThis project is licensed under the terms of the MIT license.',
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
