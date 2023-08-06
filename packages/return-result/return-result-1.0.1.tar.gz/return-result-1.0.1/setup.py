# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['return_result']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'return-result',
    'version': '1.0.1',
    'description': "This defines a decorator that causes the 'result' variable to be returned when there is no explicit return",
    'long_description': '[![PyPI version](https://img.shields.io/pypi/v/return-result)](https://pypi.org/project/return-result/)\n[![Python versions](https://img.shields.io/pypi/pyversions/return-result.svg)](https://pypi.org/project/return-result/)\n[![Black codestyle](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n# return-result\n\nThis defines a decorator that causes the variable `result` to be automatically returned from a function when there is no return statement. \n\nInspired by the [Nim feature](https://nim-by-example.github.io/variables/result/) that does the same thing.\n# Example\n\n```python\n>>> from return_result import return_result\n>>> @return_result\n... def test():\n...     result = "Works!"\n>>> test()\n\'Works!\'\n```\n\n# Requirements\n\nPython 3.6+\n',
    'author': 'Bolun Thompson',
    'author_email': 'abolunthompson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bolunthompson/return-result',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
