# Trello API - Async Python SDK client (using aiohttp)

<p align="center">
<img src="https://img.shields.io/badge/tests-pytest-orange?style=for-the-badge" alt="pytest"/>
<img src="https://img.shields.io/badge/async-asyncio, aiohttp-green?style=for-the-badge" alt="asyncio, aiohttp"/>
<a href="https://t.me/herr_horror"><img src="https://img.shields.io/badge/Telegram Chat-@herr_horror-2CA5E0.svg?logo=telegram&style=for-the-badge" alt="Chat on Telegram"/></a>
<img src="https://img.shields.io/badge/version-v.0.0.2-green?style=for-the-badge" alt="Last Release"/>
</p>


Simple and fast client to call rest-api endpoints `https://trello.com/1/` using aiohttp package.  

View at:
https://pypi.org/project/python-trello-api/


## How to install
```bash
pip3 install python-trello-api
```


## Usage

Main example:
```python
from api_trello import TrelloJson, TrelloWebHook, TrelloCard, TrelloList, Display, Member, Client, TrelloException
from loguru import logger as log
import asyncio

APP_HOSTNAME = "https://YOUR_HOSTNAME.ngrok.io"
trello_api_key = "YOUR_API_KEY"
trello_board_id = "5f43db65a1d25218690c062b"
trello_token = "YOUR_TOKEN"

trello_json = TrelloJson(api_key=trello_api_key,
        token=trello_token,
        board_id=trello_board_id)

trello = Client(api_key=trello_api_key,
        token=trello_token,
        board_id=trello_board_id)

async def main_async():
    response = await trello_json.get_lists()
    log.error(response)  #  [{'id': '5f43db65a1d25218690c062c', 'name': 'Новая задача', 'closed': False, 'pos': 16384, 'softLimit': None, 'idBoard': '5f43db65a1d25218690c062b', 'subscribed': False}, {'id': '5f43db65a1d25218690c062d', 'name': 'В работе', 'closed': False, 'pos': 32768, 'softLimit': None, 'idBoard': '5f43db65a1d25218690c062b', 'subscribed': False}, {'id': '5f43ebe557a419018bb34b4b', 'name': 'Требуется помощь IT', 'closed': False, 'pos': 40960, 'softLimit': None, 'idBoard': '5f43db65a1d25218690c062b', 'subscribed': False}, {'id': '5f43db65a1d25218690c062e', 'name': 'Завершена', 'closed': False, 'pos': 106496, 'softLimit': None, 'idBoard': '5f43db65a1d25218690c062b', 'subscribed': False}]

    response = await trello.get_lists()
    log.error(response)  #  [TrelloList(id='5f43db65a1d25218690c062c', name='Новая задача', type=None, text=None), TrelloList(id='5f43db65a1d25218690c062d', name='В работе', type=None, text=None), TrelloList(id='5f43ebe557a419018bb34b4b', name='Требуется помощь IT', type=None, text=None), TrelloList(id='5f43db65a1d25218690c062e', name='Завершена', type=None, text=None)]

    response = await trello_json.add_member("5fc10d349569a54078da50fe", "5a214fe083df8aa8c81899e8")
    log.error(response)  #  [{'id': '5f490ec27cd5990eeb8e53f2', 'username': 'bot_user1', 'activityBlocked': False, 'avatarHash': None, 'avatarUrl': None, 'fullName': 'BOT_Trello', 'idMemberReferrer': None, 'initials': 'B', 'nonPublic': {}, 'nonPublicAvailable': True}, {'id': '5a214fe083df8aa8c81899e8', 'username': 'herr_horror', 'activityBlocked': False, 'avatarHash': '907ce73a28929a01448eca6e46abdc1b', 'avatarUrl': 'https://trello-members.s3.amazonaws.com/5a214fe083df8aa8c81899e8/907ce73a28929a01448eca6e46abdc1b', 'fullName': 'herr_horror', 'idMemberReferrer': None, 'initials': 'H', 'nonPublic': {}, 'nonPublicAvailable': True}]

    response = await trello.add_member("5fc10d349569a54078da50fe", "5a214fe083df8aa8c81899e8")
    log.error(response)  # [Member(id='5a214fe083df8aa8c81899e8', type=None, username='herr_horror', text=None, full_name='herr_horror')]


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async())
```




### Docs
1. How to publish pypi package [Medium article in Russian](https://medium.com/nuances-of-programming/python-%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D1%8F-%D0%B2%D0%B0%D1%88%D0%B8%D1%85-%D0%BF%D0%B0%D0%BA%D0%B5%D1%82%D0%BE%D0%B2-%D0%B2-pypi-11dd3216581c)


## Dependencies
TODO


## Disclaimer
This project and its author is neither associated, nor affiliated with [Atlassian](https://atlassian.com/) or [Trello](https://trello.com/) in anyway.
See License section for more details.


## License

This project is released under the [GNU LESSER GENERAL PUBLIC LICENSE][link-license] License.

[link-author]: https://github.com/DmitriyKalekin
[link-repo]: https://github.com/DmitriyKalekin/python-trello-api
[link-pygramtic]: https://github.com/devtud/pygramtic
[link-issues]: https://github.com/DmitriyKalekin/python-trello-api/issues
[link-contributors]: https://github.com/DmitriyKalekin/python-trello-api/contributors
[link-docs]: https://telegram-bot-api.readme.io/docs
[link-license]: https://github.com/DmitriyKalekin/python-trello-api/blob/main/LICENSE
[link-trello-api]: https://developer.atlassian.com/cloud/trello/rest/api-group-actions/

