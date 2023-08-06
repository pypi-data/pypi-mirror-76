# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['composetools']
entry_points = \
{'console_scripts': ['test = tests:run', 'tests = tests:run']}

setup_kwargs = {
    'name': 'composetools',
    'version': '0.1.0',
    'description': 'Utility functions for common tasks when composing functions.',
    'long_description': '# composetools\n\nUtility functions for Pythonic function composition.\nBYO `compose()` implementation.\n\n## Install\n\n```\npip install composetools\n```\n\n## Examples\n\n```python\nfrom funcy import compose, rcompose\n\nfrom composetools import unique, flat, sort\n\n\n# Get unique items from nested iterables.\ncompose(sort, flat, unique)([[1, 2, 3], [4, 3, 2]])  # [1, 2, 3, 4]\n\n\n# Get lines of a file.\nfrom pathlib import Path\nget_lines = rcompose(\n    Path,\n    Path.expanduser,\n    Path.resolve,\n    Path.read_text,\n    str.splitlines,\n)\nget_lines("~/.gitconfig")\n```\n\n## Functions\n\n* `tap` - Call a function but don\'t return the result, eg. `tap(lambda x: print(x))(4) == 4`\n* `each` - Curried version of `map`.\n* `keep` - Curried version of `filter`.\n* `drop` - Curried version of `itertools.filterfalse`.\n* `sort` - Curried version of `sorted`.\n* `flat` - Flatten an arbitrarily nested iterable.\n* `unique` - Yield unique items of an iterable.\n\n## Develop\n\n```\n$ git clone https://github.com/SeparateRecords/python-composetools\n$ poetry install\n$ poetry run tests\n```\n\n## Licence\n\nISC\n',
    'author': 'SeparateRecords',
    'author_email': 'me@rob.ac',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
