import os
import time
import requests
import asyncio
import telegram

from dotenv import load_dotenv


async def main(new_attempts, token, chat_id_tg):
    bot = telegram.Bot(token)
    result = get_work_result(new_attempts)

    async with bot:
        await bot.send_message(text='У вас была проверена работа "{}" \n {} \n {}'.format(
            new_attempts['lesson_title'], result, new_attempts['lesson_url']), chat_id=chat_id_tg)


def get_work_result(new_attempts):
    if new_attempts['is_negative']:
        return 'Приступайте к следующему уроку'
    else:
        return 'В работе присутствуют ошибки'


def get_request_status(response_details):

    if response_details.get('error'):
        raise requests.HTTPError(response_details['error']['error_code'])


if __name__ == '__main__':
    load_dotenv()
    token = os.environ["TOKEN"]
    chat_id_tg = os.environ["CHAT_ID_TG"]
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': 'Token ee17a19ea5ed9a5817e85ff4374211f78de8fc63'
        }

    params = {
        'timestamp': '1555493856',
        }

    try:
        while True:
            response_details = requests.get(url, headers=headers, params=params, timeout=60).json()
            get_request_status(response_details)
            new_attempts = response_details['new_attempts'][0]
            params['timestamp'] = new_attempts['timestamp']
            asyncio.run(main(new_attempts, token, chat_id_tg))

    except requests.exceptions.ReadTimeout:
            requests.get(url, headers=headers, params=params, timeout=0.001)
            time.sleep(60)

    except ConnectionError:
            time.sleep(60)
