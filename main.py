import os
import time
import requests
import telegram
import argparse

from dotenv import load_dotenv


def main(new_attempts, token_tg, chat_id_tg):
    bot = telegram.Bot(token_tg)
    result = get_work_result(new_attempts)
    bot.send_message(text='У вас была проверена работа "{}" \n {} \n {}'.format(
        new_attempts['lesson_title'], result, new_attempts['lesson_url']), chat_id=chat_id_tg
        )


def get_work_result(new_attempts):
    if new_attempts['is_negative']:
        return 'Приступайте к следующему уроку'
    else:
        return 'В работе присутствуют ошибки'


def get_request_status(response_details):

    if response_details.get('error'):
        raise requests.HTTPError(response_details['error']['error_code'])


def get_args():
    parser = argparse.ArgumentParser(description='Запуск телегарм бота')
    parser.add_argument('--token_tg', default=os.environ["TOKEN_TG"], help='Введите TOKEN_TG')
    parser.add_argument('--chat_id_tg', default=os.environ["CHAT_ID_TG"], help='Введите CHAT_ID_TG')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    load_dotenv()
    args = get_args()
    token_tg = args.token_tg
    chat_id_tg = args.chat_id_tg
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': 'Token ee17a19ea5ed9a5817e85ff4374211f78de8fc63'
        }

    params = {
        'timestamp': time.time(),
        }

    try:
        while True:
            response_details = requests.get(url, headers=headers, params=params, timeout=60).json()
            get_request_status(response_details)
            new_verification_attempt = response_details['new_attempts'][0]
            params['timestamp'] = new_verification_attempt['timestamp']
            main(new_verification_attempt, token_tg, chat_id_tg)

    except requests.exceptions.ReadTimeout:
            requests.get(url, headers=headers, params=params, timeout=0.001)

    except ConnectionError:
            time.sleep(60)
    
    except KeyError:
            time.sleep(60)
