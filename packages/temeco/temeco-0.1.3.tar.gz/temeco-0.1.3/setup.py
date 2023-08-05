# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temeco']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'temeco',
    'version': '0.1.3',
    'description': 'A small package handling telegram message copying preserving text entities',
    'long_description': '# Telegram Message Copy (TeMeCo)\n\n[![EO principles respected here](https://www.elegantobjects.org/badge.svg)](https://www.elegantobjects.org)\n[![Build Status](https://travis-ci.org/monomonedula/temeco.svg?branch=master)](https://travis-ci.org/monomonedula/temeco)\n[![codecov](https://codecov.io/gh/monomonedula/temeco/branch/master/graph/badge.svg)](https://codecov.io/gh/monomonedula/temeco)\n[![PyPI version](https://badge.fury.io/py/temeco.svg)](https://badge.fury.io/py/temeco)\n\n`temeco` is a simple Telegram message entities to html translator.\nTelegram Bot API makes it cumbersome fro bots to copy a user\'s message\npreserving its entities, since it is currently impossible for a bot to send\nentities directly along with a message, \nso it needs to translate a message with entities into HTML or Markdown.\n\nThis little package solves this problem and provides a convenient way\nto translate a message with entities to HTML. \n\n`TelegramUTF16Text` class is also aware of the fact that Telegram calculates\n offsets for entities using UTF-16 encoding. \n This comes into play when text being copied contains symbols which have different lengths\n in UTF-8 and UTF-16 code units, like emojis.\n \n ## Installation\n `pip install temeco`\n \n ## Usage:\n ```python\nfrom temeco.temeco import BasicEntity, TelegramUTF16Text, HtmlFromMsg\n\ntext = (\n    "dolorem ipsum, quia dolor sit, 🔥🚒 amet, consectetur, adipisci velit, sed quia 🙃 non numquam eius modi"\n    " tempora incidunt, 🙊\\nut labore et dolore magnam aliquam quaerat voluptatem."\n)\nHtmlFromMsg(\n    msg_txt=TelegramUTF16Text(text),\n    entities=[\n        BasicEntity(\n            type="bold", offset=8, length=5, msg_text=TelegramUTF16Text(text)\n        ),\n        BasicEntity(\n            type="code", offset=55, length=8, msg_text=TelegramUTF16Text(text)\n        ),\n        BasicEntity(\n            type="text_link",\n            offset=64,\n            length=5,\n            data={"url": "http://google.com/"},\n            msg_text=TelegramUTF16Text(text),\n        ),\n        BasicEntity(\n            type="italic",\n            offset=153,\n            length=7,\n            msg_text=TelegramUTF16Text(text),\n        ),\n    ],\n).as_str()\n```\n \n ## Note:\n `BasicEntity` class supports the following types of entities:\n - `bold`\n - `italic`\n - `text_link`\n - `code` (monospace text)\n - `pre` (preformatted text)\n\nEntities like hashtags and usernames are copied as is, since Telegram recognizes them\nwithout extra code.\n\nYou may create your own class implementing `Entity` interface and use it instead of \nBasicEntity.\n ',
    'author': 'monomonedula',
    'author_email': 'valh@tuta.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monomonedula/temeco',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
