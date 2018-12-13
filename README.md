MovieBot
========

MovieBot - это бот для Telegramm, который будет рекомендовать фильмы для просмотра в кинотеатрах, а также информировать о премьерах.

Подоробнее о проекте по ссылке: <a href="https://docs.google.com/document/d/1-1Dnsv8-O4cPDdo2XeNWVOTzfxnV6UkUa3NVsY_NkIg/edit?usp=sharing">Описание проекта</a>

Установка
=========

Создайте виртуальное окружение и активируйте его. Потом в виртуальном окружении выполните:

.. code-block::text
    
    pip install -r requirements.txt 

Настройка
=========

Создайте файл settings.py и добавьте туда следующие настройки:

.. code-block::python
    
    PROXY = {'proxy_url' : 'socks5://ВАШ_SOCKS_ПРОКСИ:1080',
        'urllib3_proxy_kwargs':{'username':'ЛОГИН','password': 'ПАРОЛЬ'}}

    API_KEY = 'API ключ который вы получили у BotFather'

Запуск
======

В активированном виртуальном окружении запустите:

.. code-block::text

    python movie_bot.py