# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geosardine']

package_data = \
{'': ['*']}

install_requires = \
['affine>=2.3.0,<3.0.0',
 'fiona',
 'gdal',
 'numpy>=1.18,<2.0',
 'rasterio',
 'shapely>=1.6.4,<2.0.0']

setup_kwargs = {
    'name': 'geosardine',
    'version': '0.2.1a0',
    'description': 'Spatial operations extend fiona and rasterio',
    'long_description': None,
    'author': 'Sahit Tuntas Sadono',
    'author_email': '26474008+sahitono@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
