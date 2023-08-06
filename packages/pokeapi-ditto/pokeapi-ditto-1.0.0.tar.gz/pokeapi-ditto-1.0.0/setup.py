# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pokeapi_ditto', 'pokeapi_ditto.commands']

package_data = \
{'': ['*']}

install_requires = \
['genson>=1.0,<2.0',
 'odictliteral>=1.0,<2.0',
 'requests>=2.19,<3.0',
 'tqdm>=4.26,<5.0',
 'yarl>=1.2,<2.0']

entry_points = \
{'console_scripts': ['ditto = pokeapi_ditto.main:main']}

setup_kwargs = {
    'name': 'pokeapi-ditto',
    'version': '1.0.0',
    'description': 'Ditto is a command line tool for performing meta operations over PokéAPI data.',
    'long_description': '# Ditto <a href="https://pokeapi.co/api/v2/pokemon/ditto"><img src=\'https://veekun.com/dex/media/pokemon/global-link/132.png\' height=50px/></a>\n\nThis repository contains:\n\n - `ditto clone`: a script to crawl an instance of PokeAPI and download all data\n - `ditto analyze`: a script to generate a JSON schema of the above data\n - `ditto transform`: a script to apply a new base url to the above data and schema\n\n## Usage\n\n```sh\npip install pokeapi-ditto\nditto --help\n```\n\n## Development\n\n```sh\npoetry install\npoetry run ditto --help\n```\n\n## Docker\n\nYou should have a PokeApi server running on `localhost:80`.\n\n```sh\n# runs clone, analyze, and transform all in one step\ndocker-compose up --build\n```\n',
    'author': 'Sargun Vohra',
    'author_email': 'sargun.vohra@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PokeAPI/ditto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
