# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_sketch']

package_data = \
{'': ['*']}

install_requires = \
['pyfiglet>=0.8.post1,<0.9', 'pyinquirer>=1.0.3,<2.0.0']

entry_points = \
{'console_scripts': ['flask-sketch = flask_sketch.__main__:flask_sketch']}

setup_kwargs = {
    'name': 'flask-sketch',
    'version': '0.2.2',
    'description': 'A CLI for autogenerate folder structure for Flask applications',
    'long_description': None,
    'author': 'Eric Souza',
    'author_email': 'ericsouza0801@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
