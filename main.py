import requests
import telegram
from loguru import logger
from environs import Env


def main():
    env = Env()
    env.read_env()
    headers = {
        'Authorization': env('DEVMAN_TOKEN')
    }

    token = env('BOT_TOKEN')
    chat_id = env('CHAT_ID')
    bot = telegram.Bot(token=token)

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
        except requests.exceptions.ReadTimeout:
            logger.warning('Превышено время оэидания')
        except requests.exceptions.ConnectionError:
            logger.warning('Соединение разорвано')


if __name__ == '__main__':
    main()