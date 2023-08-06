# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiktok_bot',
 'tiktok_bot.api',
 'tiktok_bot.bot',
 'tiktok_bot.client',
 'tiktok_bot.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.7.4,<0.8.0',
 'loguru>=0.3.2,<0.4.0',
 'pydantic>=0.32.2,<0.33.0',
 'tqdm>=4.38.0,<5.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'tiktok-bot',
    'version': '0.6.4',
    'description': 'Tik Tok API',
    'long_description': '# This project is no longer under development.\n# A NEW project is being developed here: [sudoguy/tiktokpy](https://github.com/sudoguy/tiktokpy/)\n\n---\n\n<h1 align="center" style="font-size: 3rem;">\ntiktok-bot\n</h1>\n<p align="center">\n <em>The most intelligent TikTok bot for Python.</em></p>\n\n<p align="center">\n<a href="https://travis-ci.org/sudoguy/tiktok_bot">\n    <img src="https://travis-ci.org/sudoguy/tiktok_bot.svg?branch=master" alt="Build Status">\n</a>\n<a href="https://pepy.tech/project/tiktok-bot">\n    <img src="https://pepy.tech/badge/tiktok-bot" alt="Downloads">\n</a>\n<a href="https://pypi.org/project/tiktok-bot/">\n    <img src="https://badge.fury.io/py/tiktok-bot.svg" alt="Package version">\n</a>\n</p>\n\n\n**Note**: *This project should be considered as an **"alpha"** release.*\n\n---\n\n## Quickstart\n\n```python\nfrom tiktok_bot import TikTokBot\n\nbot = TikTokBot()\n\n# getting your feed (list of posts)\nmy_feed = bot.list_for_you_feed(count=25)\n\npopular_posts = [post for post in my_feed if post.statistics.play_count > 1_000_000]\n\n# extract video urls without watermark (every post has helpers)\nurls = [post.video_url_without_watermark for post in popular_posts]\n\n# searching videos by hashtag name\nposts = bot.search_posts_by_hashtag("cat", count=50)\n```\n\n## Installation\n\nInstall with pip:\n\n```shell\npip install tiktok-bot\n```\n\ntiktok-bot requires Python 3.6+\n',
    'author': 'Evgeny Kemerov',
    'author_email': 'eskemerov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sudoguy/tiktok_bot/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
