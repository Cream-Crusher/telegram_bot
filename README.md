# Телеграм бот

Бот для проверки уроков.

## Запуск

* Скачайте код
* Скачайте библиотеки ```pip install -r requirements.txt```
* Заполните файл .env по образцу
```python
.env

TOKEN=Your token
CHAT_ID=Your chat id
```
##### или
* Запустите код с использованием параметров argparse

 --token_tg = Токен телеграмма
 
 --chat_id_tg = Токен чата телеграмма
 
 example:
```python
$ python main.py --token_tg 123:qwe chat_id_tg 123
```


* Запустите сайт командой ```python3 main.py``` или ```python main.py --token_tg 123:qwe chat_id_tg 123```
* Зайдите в telegram
