# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['willing_zg']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.8,<4.0.0', 'djangorestframework>=3.11.0,<4.0.0']

setup_kwargs = {
    'name': 'django-willing-zg',
    'version': '0.2.0',
    'description': '',
    'long_description': '# django-willing-zg\nA Django app to hold common utilities for Zygoat-managed applications\n\n\n## What it does\n`willing_zg` provides a means to define frontend configuration in the django settings and an API endpoint to make that configuration accessible.\n\n## Usage\n1. Add "willing_zg" to `INSTALLED_APPS` in the django settings\n\n2. Define `ZYGOAT_FRONTEND_META_CONFIG` in the django settings\n\n    ZYGOAT_FRONTEND_META_CONFIG = { "example_frontend_config": "example_value" }\n\n3. Include the willing_zg URLconf in your project\'s urls.py:\n\n    path(\'api/zygoat/\', include(\'willing_zg.urls\')),\n',
    'author': 'Bequest, Inc.',
    'author_email': 'oss@willing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
