# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['japanese_addresses']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'japanese-addresses',
    'version': '0.0.1',
    'description': '',
    'long_description': '# japanese-addresses\n\n[![Python package](https://github.com/wakamezake/japanese-addresses/workflows/Python%20package/badge.svg?branch=master)](https://github.com/wakamezake/japanese-addresses/actions?query=workflow%3A%22Python+package%22)\n[![codecov](https://codecov.io/gh/wakamezake/japanese-addresses/branch/master/graph/badge.svg)](https://codecov.io/gh/wakamezake/japanese-addresses)\n[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/wakamezake/japanese-addresses/master)\n\nParsing Japan addresses to prefectures and cities.\n\n## Installation\n\n```\npip install git+https://github.com/wakamezake/japanese-addresses.git\n```\n\n## Examples\n\n```python\nfrom japanese_addresses import separate_address\n\nparsed_address = separate_address(\'宮城県仙台市泉区市名坂字東裏97-1\')\n\nprint(parsed_address)\n"""\nParsedAddress(prefecture=\'宮城県\', city=\'\')\n"""\n```\n\n## Testing\n\n```\npip install poetry\npoetry install\npoetry run pytest\n```\n',
    'author': 'wakame',
    'author_email': 'hotwater1367@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wakamezake/japanese-addresses.git',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
