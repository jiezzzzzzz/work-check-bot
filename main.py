import requests
import telegram
from loguru import logger
from environs import Env
import logging
import time


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_token, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=tg_token)

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


log = logging.getLogger('tg_logger')


def main():
    env = Env()
    env.read_env()
    headers = {
        'Authorization': env('DEVMAN_TOKEN')
    }

    token = env('BOT_TOKEN')
    second_bot = env.bool('SECOND_BOT', False)
    chat_id = env('CHAT_ID')
    bot = telegram.Bot(token=token)

    log.setLevel(logging.WARNING)
    if second_bot:
        tg_service_token = env('TG_SERVICE_TOKEN')
        log.addHandler(TelegramLogsHandler(tg_service_token, chat_id))

    while True:
        try:
            url = 'https://dvmn.org/api/long_polling/'

            payload = {
                'timestamp': ''
            }

            response = requests.get(url, headers=headers, params=payload, timeout=60)

            response.raise_for_status()
            changes = response.json()

            if changes['status'] == 'timeout':
                payload['timestamp'] = changes['timestamp_to_request']
            elif changes['status'] == 'found':
                payload['timestamp'] = changes['last_attempt_timestamp']
                attempts = changes['new_attempts']
                for attempt in attempts:
                    if attempt['is_negative']:
                        text = f'''\
                                    Урок "{attempt["lesson_title"]}" вернулся с проверки 
                                    Нужно доработать:(
                                    Посмотреть результат можно по ссылке {attempt["lesson_url"]}'''
                    else:
                        text = f'''\
                                    Урок "{attempt["lesson_title"]}" вернулся с проверки' 
                                    Лучше ничего не сделать :)
                                    Посмотреть результат можно по ссылке {attempt["lesson_url"]}'''

                    bot.send_message(text=text, chat_id=chat_id)

        except requests.exceptions.HTTPError as error:
            logger.warning(f'HTTPError: {error}')
            log.warning(f'Я упал, HTTP error {error}')
        except requests.exceptions.ReadTimeout:
            logger.warning('Превышено время ожидания')
        except requests.exceptions.ConnectionError:
            logger.warning('Соединение разорвано')
            log.warning('Соединение разорвано, я упал')
            time.sleep(60)


if __name__ == '__main__':
    main()