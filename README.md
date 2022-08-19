# Телеграм бот

Бот для проверки уроков.

## Запуск

* Скачайте код
* Скачайте библиотеки ```pip install -r requirements.txt```
* Создайте и заполните файл .env по образцу
```python
TG_TOKEN=Your tg token
TG_CHAT_ID=Your tg chat id
DEVMAN_TOKEN=Your devman token
```
DEVMAN_TOKEN можно узнать здесь [devman token](https://dvmn.org/api/docs/)

##### или
* Запустите код с использованием параметров argparse

 --tg_token = Токен телеграмма
 
 --tg_chat_id = Токен чата телеграмма
 
 --devman_token= Токен devman
 
 example:
```python
$ python main.py --tg_token 123:qwe --tg_chat_id 123 --devman_token q1w2e3
```


* Запустите сайт командой ```python3 main.py``` или ```python main.py --tg_token 123:qwe --tg_chat_id 123 --devman_token q1w2e3```
* Зайдите в telegram
