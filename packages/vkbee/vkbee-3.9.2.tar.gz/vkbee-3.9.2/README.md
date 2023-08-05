﻿![vkbee](https://github.com/asyncvk/vkbee/raw/master/logo.png)
<h1 align="center">VKBee - простая в использовании библиотека для взаимодействия с API ВКонтакте</h1>
<p align="center">
    <img alt="Made with Python" src="https://img.shields.io/badge/Made%20with-Python-%23FFD242?logo=python&logoColor=white">
    <img alt="Downloads" src="https://pepy.tech/badge/vkbee">
</p>

## Установка
Из PyPI:
```bash
$ pip install vkbee
```
Из GitHub (рекомендуется):
```bash
$ pip install https://github.com/asyncvk/vkbee/archive/master.zip
```
> Минимальная версия Python - 3.6

## Простой пример
```python
import asyncio
import vkbee

from vkbee import oldlong

async def main(loop):
    token = 'token'
    vk = oldlong.VkApi(token=token, loop=loop)
    longpoll = oldlong.BotLongpoll(vk, 'groupid', 10)

    async for event in longpoll.events():
        user_id = event['object']['message']['from_id']
        message_text = event['object']['message']['text']
        await vkbee.VkApi.call(vk, 'messages.send', {'user_id': user_id, 'message': message_text, 'random_id': 0})

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
```

Больше примеров имеется в [документации](https://github.com/asyncvk/vkbee/blob/master/docs/docs.md)
