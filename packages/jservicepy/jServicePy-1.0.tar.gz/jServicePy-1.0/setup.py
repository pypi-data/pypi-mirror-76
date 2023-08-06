# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jservicepy']
install_requires = \
['argparse>=1.4.0,<2.0.0',
 'datetime>=4.3,<5.0',
 'requests>=2.24.0,<3.0.0',
 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'jservicepy',
    'version': '1.0',
    'description': 'API wrapper for jService (comes with a commmand-line game implementation!)',
    'long_description': '# jServicePy\nAPI wrapper for jService (comes with a commmand-line game implementation!)\n\n![jService Logo](https://jservice.io/assets/trebek-503ecf6eafde622b2c3e2dfebb13cc30.png)\n\nA wrapper for [jService](https://jservice.io) and a small command-line based version of Jeopardy using said wrapper with ANSI escape codes.\n\n## Examples\n### API\n```python\nfrom jservicepy import jService\njeopardy = jService() # <- If you\'re running your own instance, put your base URL in here\nclues = jeopardy.clues()\nfor clue in clues:\n    print(clue.question + \':\', clue.answer, \'| $\' + str(clue.value))\n```\n### CLI\n```\npython -m jservicepy -h\nusage: jServicePy [-h] [-c NUMBER] [-r NUMBER] [-v]\n\nPlay Jeopardy in your terminal! Powered by @sottenad\'s jService\n[https://github.com/sottenad/jService] (v1.0)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -c NUMBER, --categories NUMBER\n                        Answer questions from a NUMBER of random categories.\n  -r NUMBER, --random NUMBER\n                        Answer a NUMBER of random questions\n  -v, --version         show program\'s version number and exit\n```\n## Application Programming Interfacte Documentation\n### class jService\n#### __init__\nInitialize jService.\n###### Args:\n* baseURL (str, optional): Base URL to send requests to; use if you are making calls to your own instance of jService. Defaults to "https://jservice.io".\n        \n#### categories\nGet a list of categories.\n\n###### Args:\n* count (int, optional): Amount of categories to return, limited to 100 at a time. Defaults to 1.\noffset (int, optional): Offsets the starting ID of categories returned. Useful in pagination. Defaults to 0.\n\n###### Returns:\n* list: A list of Category dataclasses.\n        \n#### category\nGet a category.\n\n###### Args:\n* id (int): The ID of the category to return.\n\n###### Returns:\n* Category: A dataclass containing the cateory ID, title, number of clues, and list of clues for the category.\n        \n#### clues\nGet a list of clues.\n\n###### Args:\n* value (int, optional): The value of the clue in dollars.\n* category (int, optional): The id of the category you want to return.\n* min_date (datetime, optional): Earliest date to show, based on original air date.\n* max_date (datetime, optional): Latest date to show, based on original air date.\n* offset (int, optional): Offsets the returned clues. Useful in pagination.\n\n##### Returns:\n* list: A list of Clue dataclasses.\n        \n#### random\nGet random clues.\n\n###### Args:\n* count (int, optional): Amount of clues to return, limited to 100 at a time. Defaults to 1.\n\n###### Returns:\n* list: A list of Clue dataclasses.',
    'author': 'Kyle Anthony Williams',
    'author_email': 'kyle.anthony.williams2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SuperSonicHub1/jServicePy',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
