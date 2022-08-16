import os
import time
import requests
import asyncio
import telegram

from dotenv import load_dotenv


async def main(new_attempts, token, chat_id):
    bot = telegram.Bot(token)
    result = work_result(new_attempts)

    async with bot:
        await bot.send_message(text='У вас была проверена работа "{}" \n {} \n {}'.format(
            new_attempts['lesson_title'], result, new_attempts['lesson_url']), chat_id=chat_id)


def work_result(new_attempts):
    if new_attempts['is_negative'] is True:
        result = 'Приступайте к следующему уроку'
    else:
        result = 'В работе присутствуют ошибки'
    return result


if __name__ == '__main__':
    load_dotenv()
    token = os.environ["TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': 'Token ee17a19ea5ed9a5817e85ff4374211f78de8fc63'
        }

    params = {
        'timestamp': '1555493856',
        'timeout': 1
        }

    try:
        while True:
            response = requests.get(url, headers=headers, params=params, timeout=60).json()
            new_attempts = response['new_attempts'][0]
            params['timestamp'] = new_attempts['timestamp']
            asyncio.run(main(new_attempts, token, chat_id))

    except requests.exceptions.ReadTimeout:
            time.sleep(60)

    except ConnectionError:
            time.sleep(60)
