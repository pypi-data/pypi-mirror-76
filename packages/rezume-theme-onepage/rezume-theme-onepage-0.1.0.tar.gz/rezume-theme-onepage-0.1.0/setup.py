# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rezume_theme_onepage']

package_data = \
{'': ['*'], 'rezume_theme_onepage': ['assets/*']}

install_requires = \
['pybars3>=0.9.7,<0.10.0']

setup_kwargs = {
    'name': 'rezume-theme-onepage',
    'version': '0.1.0',
    'description': 'A rezume theme port of jsonresume-theme-onepage',
    'long_description': 'rezume-theme-onepage\n====================\n\nThis is a Rezume theme port of ``jsonresume-theme-onepage`` which is a compact theme\ndesigned for printing.\n',
    'author': 'Abdulhakeem Shaibu',
    'author_email': 'hkmshb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hkmshb/rezume-themes.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
