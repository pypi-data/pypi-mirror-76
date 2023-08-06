# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['avajana']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'avajana',
    'version': '0.2.1',
    'description': 'Avajana helps chatbot to express/emulate indirect expressions. Currently, it helps with chatbot bubbling. The bubble that happen to the other end of receipient when someone is typing.',
    'long_description': '# Avajana\nAvajana helps chatbot to express/emulate indirect expressions. Currently, it helps with chatbot bubbling. The bubble that happen to the other end of receipient when someone is typing.\n\n## Get Started\n```bash\n$ pip install avajana\n```\n\n> Avajana (อวัจนะ) means non-verbal in Thai. ',
    'author': 'Nutchanon Ninyawee',
    'author_email': 'me@nutchanon.org',
    'maintainer': 'Nutchanon Ninyawee',
    'maintainer_email': 'me@nutchanon.org',
    'url': 'https://github.com/sakuguru/avajana',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
