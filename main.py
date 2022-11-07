import os
import time
import requests
import telegram
import argparse
import logging

from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


class Bot_tel:

    def __init__(self, tg_token):
        self.bot = telegram.Bot(tg_token)


def send_notification_tel(new_attempts, bot, tg_chat_id):
    result = get_work_result(new_attempts)
    bot.send_message(text='У вас была проверена работа "{}" \n {} \n {}'.format(
        new_attempts['lesson_title'], result, new_attempts['lesson_url']), chat_id=tg_chat_id
        )
    logging.info('Бот отправил сообщение')


def get_work_result(new_attempts):
    if new_attempts['is_negative']:
        return 'Приступайте к следующему уроку'
    else:
        return 'В работе присутствуют ошибки'


def get_args():
    parser = argparse.ArgumentParser(description='Запуск телегарм бота')
    parser.add_argument('--tg_token', default=os.environ["TG_TOKEN"], help='Введите TG_TOKEN')
    parser.add_argument('--tg_chat_id', default=os.environ["TG_CHAT_ID"], help='Введите TG_CHAT_ID')
    parser.add_argument('--devman_token', default=os.environ["DEVMAN_TOKEN"], help='Введите DEVMAN_TOKEN')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    load_dotenv()
    args = get_args()
    tg_token = args.tg_token
    tg_chat_id = args.tg_chat_id
    devman_token = args.devman_token
    url = 'https://dvmn.org/api/long_polling/'
    tg_bot = Bot_tel(tg_token).bot
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    handler = RotatingFileHandler("app.log", maxBytes=2000, backupCount=2)
    logger.addHandler(handler)
    logger.info("Бот запущен")

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
                send_notification_tel(new_verification_attempt, tg_bot, tg_chat_id)
            else:
                params['timestamp'] = time.time()

        except requests.exceptions.ReadTimeout:
                requests.get(url, headers=headers, params=params, timeout=0.001)

        except ConnectionError:
                time.sleep(60)
