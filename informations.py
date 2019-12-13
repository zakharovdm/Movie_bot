import logging
import requests
import imdb
import handlers
from movie_bot import reply_actor_photo, reply_box_office, reply_description


def get_actor_by_name(bot, update, user_data):
    """Задает вопрос, "Какого актера найти".

    После нажатия кнопки "Поиск актера",
    вступает в диалог с пользователем,
    получает имя и фамилию актера.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    question = 'Какого актера найти?'
    logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
    print(f"""
              User: {update.message.chat.username},
              Chat id: {update.message.chat.id},
              Message: {update.message.text}
            """)
    update.message.reply_text(question)
    return handlers.SEARCH_ACTOR


def get_movie_by_name(bot, update, user_data):
    """Задает вопрос, "Какой фильм найти".

    После нажатия кнопки "Поиск фильма",
    вступает в диалог с пользователем,
    получает название фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    question = 'Какой фильм найти?'
    logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
    print(f"""
              User: {update.message.chat.username},
              Chat id: {update.message.chat.id},
              Message: {update.message.text}
            """)
    update.message.reply_text(question)
    return handlers.SEARCH_MOVIE


def get_actor_TMDB_id(bot, update, user_data):
    """Получение id актера на API TMDB.
        Обращаемся к API TMDB.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    try:
        query = update.message.text
        url = "https://api.themoviedb.org/3/search/person"
        params = {
            "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
            "language": "en-US",
            "query": f"""{query}""",
            "page": 1,
            "include_adult": "false"
        }
        result = requests.get(url, params=params)
        info_movie_TMDB = result.json()
        TMDB_actor_id = info_movie_TMDB["results"][0]["id"]
        reply_actor_photo(bot, update, user_data, TMDB_actor_id)
    except IndexError:
        update.message.reply_text('Ничего не найдено, проверьте запрос.')
    return handlers.CHOOSING


def get_movie_poster(bot, update, user_data, TMDB_id):
    """Выдача постера к фильму.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    movie_id = TMDB_id
    url = f"""https://api.themoviedb.org/3/movie/{movie_id}"""
    params = {
        "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US"
    }
    result = requests.get(url, params=params)
    poster_json = result.json()
    poster_file = poster_json["poster_path"]
    poster_url = f"""https://image.tmdb.org/t/p/w500{poster_file}"""
    bot.send_photo(chat_id=update.message.chat.id, photo=poster_url)


def get_movie_id(bot, update, user_data, TMDB_id):
    """Обращается к базе данных IMDb
    для получения id фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    try:
        ia = imdb.IMDb()
        user_query = update.message.text
        user_data['movie'] = user_query
        movie = ia.search_movie(user_query)
        movie_id = movie[0].movieID
        user_data = ia.get_movie(movie_id)
        logging.info(f"""
                    User: {update.message.chat.username},
                    Chat id: {update.message.chat.id},
                    Message: {update.message.text}
                """)
        print(f"""
                User: {update.message.chat.username},
                Chat id: {update.message.chat.id},
                Message: {update.message.text}
            """)
        get_movie_poster(bot, update, user_data, TMDB_id)
        reply_description(bot, update, user_data, TMDB_id)
    except IndexError:
        update.message.reply_text('Ничего не найдено, проверьте запрос.')
    return handlers.CHOOSING


def get_box_office(bot, update, user_data, TMDB_id):
    """Выдача сборов фильма.
        Обращаемся к API TMDB.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    movie_id = TMDB_id
    url = f"""https://api.themoviedb.org/3/movie/{movie_id}"""
    params = {
        "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US"
    }
    result = requests.get(url, params=params)
    movie_details = result.json()
    user_data = movie_details["revenue"]
    reply_box_office(bot, update, user_data, TMDB_id)


def get_movie_TMDB_id(bot, update, user_data):
    """Получение id фильма на API TMDB.
        Обращаемся к API TMDB.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    query = update.message.text
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US",
        "query": query,
        "page": 1,
        "include_adult": "false"
    }
    result = requests.get(url, params=params)
    info_movie_TMDB = result.json()
    TMDB_id = info_movie_TMDB["results"][0]["id"]
    get_movie_id(bot, update, user_data, TMDB_id)
    get_box_office(bot, update, user_data, TMDB_id)


def get_location(bot, update, user_data):
    longitude = update.message.location['longitude']
    latitude = update.message.location['latitude']
    url = 'https://geocode-maps.yandex.ru/1.x'
    params = {
        'apikey': '6856902f-25a4-4e4a-8b85-dffe3ded05f3',
        'format': 'json',
        'geocode': f'{longitude},{latitude}',
        'kind': 'house',
        'results': 1
    }
    result = requests.get(url, params=params)
    address = result.json()
    location = (address['response']['GeoObjectCollection']['featureMember'][0]
                ['GeoObject']['metaDataProperty']
                ['GeocoderMetaData']['text'])
    update.message.reply_text(location)
    return handlers.CHOOSING
