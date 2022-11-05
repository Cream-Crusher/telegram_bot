import os
import time
import requests
import telegram

from dotenv import load_dotenv


def send_notification_tel(new_attempts, tg_token, tg_chat_id):
    bot = telegram.Bot(tg_token)
    result = get_work_result(new_attempts)
    bot.send_message(text='У вас была проверена работа "{}" \n {} \n {}'.format(
        new_attempts['lesson_title'], result, new_attempts['lesson_url']), chat_id=tg_chat_id
        )


def get_work_result(new_attempts):
    if new_attempts['is_negative']:
        return 'Приступайте к следующему уроку'
    else:
        return 'В работе присутствуют ошибки'


if __name__ == '__main__':
    load_dotenv()
    tg_token = os.environ["TG_TOKEN"]
    tg_chat_id = os.environ["TG_CHAT_ID"]
    devman_token = os.environ["DEVMAN_TOKEN"]
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': 'Token {}'.format(devman_token)
        }

    params = {
        'timestamp': time.time(),
        }

    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=60)
            response.raise_for_status()
            response_details = response.json()

            if response_details['status'] == 'found':
                new_verification_attempt = response_details['new_attempts'][0]
                params['timestamp'] = new_verification_attempt['timestamp']
                send_notification_tel(new_verification_attempt, tg_token, tg_chat_id)
            else:
                params['timestamp'] = time.time()

        except requests.exceptions.ReadTimeout:
                requests.get(url, headers=headers, params=params, timeout=0.001)

        except ConnectionError:
                time.sleep(60)
