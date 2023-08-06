# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kde_account_oauth_client',
 'kde_account_oauth_client.management',
 'kde_account_oauth_client.management.commands',
 'kde_account_oauth_client.migrations']

package_data = \
{'': ['*'], 'kde_account_oauth_client': ['templates/blender_id_oauth_client/*']}

install_requires = \
['Django>=2.1,<3.1.0', 'requests-oauthlib>=1.0,<2.0']

setup_kwargs = {
    'name': 'kde-account-oauth-client',
    'version': '0.9.3',
    'description': 'Django app for using KDE Account as OAuth2 authentication service.',
    'long_description': None,
    'author': 'Sybren A. Stüvel',
    'author_email': 'sybren@blender.studio',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/blender-institute/kde-account-oauth-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
