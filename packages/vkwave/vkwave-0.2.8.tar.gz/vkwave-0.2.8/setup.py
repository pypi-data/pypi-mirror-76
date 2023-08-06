# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vkwave',
 'vkwave.api',
 'vkwave.api.methods',
 'vkwave.api.token',
 'vkwave.bots',
 'vkwave.bots.addons',
 'vkwave.bots.addons.easy',
 'vkwave.bots.core',
 'vkwave.bots.core.dispatching',
 'vkwave.bots.core.dispatching.cast',
 'vkwave.bots.core.dispatching.dp',
 'vkwave.bots.core.dispatching.dp.middleware',
 'vkwave.bots.core.dispatching.events',
 'vkwave.bots.core.dispatching.extensions',
 'vkwave.bots.core.dispatching.extensions.callback',
 'vkwave.bots.core.dispatching.filters',
 'vkwave.bots.core.dispatching.handler',
 'vkwave.bots.core.dispatching.router',
 'vkwave.bots.core.tokens',
 'vkwave.bots.core.types',
 'vkwave.bots.fsm',
 'vkwave.bots.storage',
 'vkwave.bots.storage.storages',
 'vkwave.bots.utils',
 'vkwave.bots.utils.keyboards',
 'vkwave.bots.utils.uploaders',
 'vkwave.client',
 'vkwave.http',
 'vkwave.longpoll',
 'vkwave.streaming',
 'vkwave.types',
 'vkwave.vkscript',
 'vkwave.vkscript.handlers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6,<4.0', 'pydantic>=1.4,<2.0', 'typing_extensions>=3.7.4,<4.0.0']

extras_require = \
{'all': ['aioredis>=1.3,<2.0'], 'storage-redis': ['aioredis>=1.3,<2.0']}

setup_kwargs = {
    'name': 'vkwave',
    'version': '0.2.8',
    'description': "Framework for building high-performance & easy to scale projects interacting with VK's API.",
    'long_description': '![vkwave](https://user-images.githubusercontent.com/28061158/75329873-7f738200-5891-11ea-9565-fd117ea4fc9e.jpg)\n\n> Пришло время избавиться от vk_api и vkbottle. VKWave здесь.\n\n[Почему VKWave?](./why_vkwave.md)\n\n```python\nfrom vkwave.bots import SimpleLongPollBot\n\nbot = SimpleLongPollBot(tokens="MyToken", group_id=123456789)\n\n@bot.message_handler()\ndef handle(_) -> str:\n    return "Hello world!"\n\nbot.run_forever()\n\n```\n[Простая библиотека для быстрого доступа к API](https://github.com/prostomarkeloff/vkwave-api)\n\n# Что это?\n\nVKWave - это фреймворк для создания производительных и лёгких в расширении проектов, взаимодействующих с API ВКонтакте.\n\nОн создан с использованием asyncio и аннотаций типов Python. Минимальная требуемая версия - это `3.7`.\n\nНаш телеграм чат - [давайте общаться!](https://t.me/vkwave)\n\nТекущий мейнтейнер этого проекта [@kesha1225](https://github.com/kesha1225)\n\n## Установка\n\nУстановить тестированную и стабильную версию с PyPi:\n\n```\npip install vkwave\n```\n\nИли с GitHub, со всеми свежими обновлениями.\n```\npip install https://github.com/fscdev/vkwave/archive/master.zip\n```\n\n\n## Производительность\n\nVKWave - это не самая быстрая библиотека, из-за нашей уверенности в том, что лёгкая настройка под себя, а также удобность при использовании во всех задач явлюятся более важными характеристиками библиотеки, чем скорость.\n\nНо мы всегда заинтересованы в улучшении производительности, поэтому не стесняйтесь делать Pull Request-ы и обсуждать проблемы производительности.\n\n## Сообщество\n\nVKWave - это очень молодой проект.\n\nПример бота с вынесением логики можно посмотреть в [VkWaveBotExample](https://github.com/kesha1225/VkWaveBotExample)\n\n### Чаты\n\nКак упоминалось ранее, у нас есть [чат в Telegram](https://t.me/vkwave).\n\nВо Вконтакте чата нет, но вы всегда можете создать свой собственный и получить его упоминание здесь.\n\n### Дополнения\n\nЕсли вы хотите создать дополнение для VKWave (например, более простой способ написания ботов, даже проще `vkwave.bots.addons.easy`), то вам следует назвать свой проект так: `vkwave-bots-really-easy`.\n\nОбщий паттерн для дополнений: `vkwave-<часть-vkwave>-<название-проекта>`.\n\n',
    'author': 'prostomarkeloff',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fscdev/vkwave',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
