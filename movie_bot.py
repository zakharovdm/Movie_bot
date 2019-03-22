import greeting
import imdb
import logging
import requests
import settings
from telegram.ext import (Updater, CommandHandler, RegexHandler,
                          ConversationHandler, MessageHandler, Filters)
from telegram import ReplyKeyboardMarkup, KeyboardButton


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='movie_bot.log'
                    )


CHOOSING, SEARCH_ACTOR, SEARCH_MOVIE = range(3)


def back_to_menu(bot, update, user_data):
    """Возвращает в главное меню.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
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
    update.message.reply_text('пока')

    return ConversationHandler.END


def greet_user(bot, update, user_data):
    """Приветсвует пользователя.

    При запуске бота, запускается клавиатура и
    дает информацию о возможностях бота.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    ave_text = 'Привет {}! {} '.format(update.message.chat.first_name,
                                       greeting.greet_text)
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
    update.message.reply_text(ave_text, reply_markup=menu_keyboard())

    return CHOOSING


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
    return SEARCH_ACTOR


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
    return SEARCH_MOVIE


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


def reply_box_office(bot, update, user_data, TMDB_id):
    box_office = user_data
    update.message.reply_text(f"""Сборы по миру: {box_office} $""")
    update.message.reply_text("Что еще ты хочешь найти? Выбирай.")
    return CHOOSING


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
    return CHOOSING


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
    return CHOOSING


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


def reply_description(bot, update, user_data, TMDB_id):
    """Выдает краткое описание фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    parts = info_movie['plot'][0].split('::')
    short_description = parts[0]
    update.message.reply_text(short_description)
    reply_directors(bot, update, user_data, TMDB_id)


def reply_directors(bot, update, user_data, TMDB_id):
    """Выдача режиссеров фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    directors_info = info_movie['director'][0:]
    name_director = []
    for directors in directors_info:
        name_director.append(directors['name'])
    producers = ', '.join(name_director)
    update.message.reply_text(f"Режиссеры: {producers}")
    reply_main_roles(bot, update, user_data, TMDB_id)


def reply_main_roles(bot, update, user_data, TMDB_id):
    """Выдача актеров в главных ролях фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    name_actors = []
    for actor in info_movie['cast'][:6]:
        name_actors.append(f"""{actor['name']} в роли {actor.currentRole}""")
    main_actors = '\n'.join(name_actors)
    update.message.reply_text(f"""В главных ролях: {main_actors}""")
    reply_release_date(bot, update, user_data, TMDB_id)


def reply_release_date(bot, update, user_data, TMDB_id):
    """Выдача даты выпуска.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    release = info_movie['original air date']
    update.message.reply_text(f"Дата выхода: {release}")


def reply_actor_photo(bot, update, user_data, TMDB_actor_id):
    """Выдача фотографии актера.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    actor_id = TMDB_actor_id
    url = f"""https://api.themoviedb.org/3/person/{actor_id}"""
    params = {
        "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US"
    }
    result = requests.get(url, params=params)
    info_actor_json = result.json()
    photo_file = info_actor_json["profile_path"]
    photo_url = f"""https://image.tmdb.org/t/p/w500{photo_file}"""
    bot.send_photo(chat_id=update.message.chat.id, photo=photo_url)
    user_data = info_actor_json
    reply_actor_birth_date(bot, update, user_data, TMDB_actor_id)


def reply_actor_birth_date(bot, update, user_data, TMDB_actor_id):
    birth_date_actor = user_data["birthday"]
    update.message.reply_text(f"""Дата рождения: {birth_date_actor}""")
    reply_actor_biography(bot, update, user_data, TMDB_actor_id)


def reply_actor_biography(bot, update, user_data, TMDB_actor_id):
    bio = user_data["biography"]
    update.message.reply_text(f"""Биография: {bio}""")
    update.message.reply_text("Что еще ты хочешь найти? Выбирай.")
    return CHOOSING


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
    return CHOOSING


def menu_keyboard():
    get_location = KeyboardButton('Определить месторасположение',
                                  request_location=True)
    film_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера'],
                                         ['Отмена', get_location]
                                         ], resize_keyboard=True
                                        )
    return film_keyboard


def talk_to_me(bot, update, user_data):
        response_user = f""" Привет {update.message.chat.first_name},
                            {greeting.greet_text}"""
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
        update.message.reply_text(response_user, reply_markup=menu_keyboard())


def main():
    """

    Запускает бот и работает с диалогом.

    """
    moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info('Бот запускается')
    print('Бот запускается')

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', greet_user,
                                     pass_user_data=True),
                      RegexHandler('^(Поиск актера)$', get_actor_by_name,
                                   pass_user_data=True),
                      RegexHandler('^(Поиск фильма)$', get_movie_by_name,
                                   pass_user_data=True)],

        states={
            CHOOSING: [RegexHandler('^(Поиск актера)$', get_actor_by_name,
                                    pass_user_data=True),
                       RegexHandler('^(Поиск фильма)$', get_movie_by_name,
                                    pass_user_data=True)],

            SEARCH_ACTOR: [RegexHandler('^(Отмена)$', back_to_menu,
                                        pass_user_data=True),
                           MessageHandler(Filters.text, get_actor_TMDB_id,
                                          pass_user_data=True)],
            SEARCH_MOVIE: [RegexHandler('^(Отмена)$', back_to_menu,
                                        pass_user_data=True),
                           MessageHandler(Filters.text, get_movie_TMDB_id,
                                          pass_user_data=True)],
        },

        fallbacks=[RegexHandler('^(Отмена)$', back_to_menu,
                                pass_user_data=True)]

    )

    dp = moviebot.dispatcher
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.location, get_location,
                                  pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me,
                                  pass_user_data=True))
    moviebot.start_polling()
    moviebot.idle()


if __name__ == "__main__":
    main()
