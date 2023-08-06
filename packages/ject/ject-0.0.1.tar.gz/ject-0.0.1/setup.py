# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ject', 'ject.length', 'ject.oneself']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ject',
    'version': '0.0.1',
    'description': 'function/lambda extensions',
    'long_description': '## ject\n##### function/lambda extensions\n\n### Usage\n```python\nfrom ject.length import length\n\ndef fun(a, b, *args, **kwargs): return a, b, args, kwargs\n\nprint(length(fun))\n```',
    'author': 'Hoyeung Wong',
    'author_email': 'hoyeungw@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydget/ject',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
