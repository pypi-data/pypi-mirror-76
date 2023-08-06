# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daml_dit_api', 'daml_dit_api.main']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp', 'dacite', 'dazl']

setup_kwargs = {
    'name': 'daml-dit-api',
    'version': '0.0.2',
    'description': 'DABL Integrations API Package',
    'long_description': None,
    'author': 'Mike Schaeffer',
    'author_email': 'mike.schaeffer@digitalasset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
