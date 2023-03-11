# Бот, проверяющий статус сданных работ на devman

---

Этот бот делает очень интерусную вещь - проверяет, что ответили на сданные работы на курсе. В зависимости от результатов, 
либо предлагает улучшить работу, либо сообщает об успешной сдаче. 

Сообщения о результатах проверки приходят в чат моментально.

Бот работает с API сайта devman и билблиотекой <code>python-telegram-bot</code>.

---

## Как запустить 

1. Получить токен [devman](https://dvmn.org/api/docs/)
2. Получить токен телеграм-бота (создав бота с помощью @BotFather)
3. Узнать свой chat id в телеграме (можно узнать, написав боту @userinfobot)
4. Установить зависимости: 

<code>pip install -r requirements.txt</code>

5. Запустить бота через терминал:

<code>python main.py</code>

Все пользовательские переменные задаются в файле .env:

```
DEVMAN_TOKEN =
BOT_TOKEN =
CHAT_ID =

```
