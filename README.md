# Бот-парсер сайта.

Задача:

Проверять сайт на наличие товара. В случае появления товара в продаже, присылать в чат бота сообщение о поступлении товара.
Также есть возможность проверять наличие товара в данный момент.

Стек:

aiogram, mechanize, lxml, sqlite3, http.cookiejar

Описание:
- atbot.py - сам бот
- config.py - файл конфигурации
- parse_web.py - программа парсер
- sqlighter.py - создание БД подписчиков бота

### Создание образа Docker

```
$ git clone https://github.com/rabenkralle/parse_bot.git
$ cd parse_bot/
$ docker build -t rush/parse_bot .
```

### Запускаем контейнер

```
$ docker run -it rush/parse_bot
```

### Обновления:

2.09.2022 

Изменен parse_web.py:
- Увеличилось количество отслеживаемых товаров. Изменен список адресов сайтов товаров. Теперь он получается автоматически.
Изменен config.py:
- Убран словарь с адресами.
- Добавлена переменная с адресом конкретного товара
- Добавлена переменная с адресом поисковой страницы для получения списка товаров для парсинга 
