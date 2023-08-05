# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comicbox', 'comicbox.metadata', 'tests']

package_data = \
{'': ['*'],
 'tests': ['test_files/Captain Science #001-cbi.cbr',
           'test_files/Captain Science #001-cbi.cbr',
           'test_files/Captain Science #001-cbi.cbr',
           'test_files/Captain Science #001-cbi.cbr',
           'test_files/Captain Science #001-cix-cbi.cbr',
           'test_files/Captain Science #001-cix-cbi.cbr',
           'test_files/Captain Science #001-cix-cbi.cbr',
           'test_files/Captain Science #001-cix-cbi.cbr',
           'test_files/Captain Science #001-comet.cbz',
           'test_files/Captain Science #001-comet.cbz',
           'test_files/Captain Science #001-comet.cbz',
           'test_files/Captain Science #001-comet.cbz',
           'test_files/Captain Science #001.cbz',
           'test_files/Captain Science #001.cbz',
           'test_files/Captain Science #001.cbz',
           'test_files/Captain Science #001.cbz']}

install_requires = \
['parse>=1.15,<2.0',
 'pycountry>=20.7.3,<21.0.0',
 'rarfile>=4.0,<5.0',
 'simplejson>=3.17,<4.0']

entry_points = \
{'console_scripts': ['comicbox = comicbox.cli:main']}

setup_kwargs = {
    'name': 'comicbox',
    'version': '0.1.0',
    'description': 'An API for reading comic archives',
    'long_description': '',
    'author': 'AJ Slater',
    'author_email': 'aj@slater.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ajslater/comicbox',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
