import greeting
import imdb
import logging
import requests
import settings


from telegram.ext import (Updater, CommandHandler, RegexHandler,
                          ConversationHandler, MessageHandler, Filters)

from telegram import ReplyKeyboardMarkup


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


def get_id_movie(bot, update, user_data):
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
        id_movie = movie[0].movieID
        user_data = ia.get_movie(id_movie)
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
        reply_description(bot, update, user_data)
    except IndexError:
        update.message.reply_text('Ничего не найдено, проверьте запрос.')
    return CHOOSING


def reply_description(bot, update, user_data):
    """Выдает краткое описание фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    update.message.reply_text(info_movie['plot'][0])
    reply_directors(bot, update, user_data)


def reply_directors(bot, update, user_data):
    """Выдача режиссера фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    ia = imdb.IMDb()
    info_movie = user_data
    director_info = info_movie['director']
    id_director = director_info[0].personID
    name_director = ia.get_person(id_director)
    update.message.reply_text(f"Режиссер: {name_director['name']}")
    reply_main_roles(bot, update, user_data)


def reply_main_roles(bot, update, user_data):
    """Выдача актеров в главных ролях фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    stars = info_movie['cast'][0:3]
    name_actors = []
    for stars_name in stars:
        name_actors.append(stars_name['name'])
    actors = ', '.join(name_actors)
    update.message.reply_text(f"В главных ролях: {actors}")
    reply_release_date(bot, update, user_data)


def reply_release_date(bot, update, user_data):
    """Выдача даты выпуска.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    release = info_movie['original air date']
    update.message.reply_text(f"Дата выхода: {release}")


def menu_keyboard():
    film_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера'],
                                         ['Отмена']
                                         ], resize_keyboard=True
                                        )
    return film_keyboard


def search_actor(bot, update, user_data):
    """Обращается к базе данных IMDb
    для поиска и выдачи информации о актере.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    try:
        ia = imdb.IMDb()
        user_query = update.message.text
        user_data['actor'] = user_query
        actor = ia.search_person(user_query)
        id_actor = actor[0].personID
        info_actor = ia.get_person(id_actor)
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
        update.message.reply_text(info_actor['bio'])
    except IndexError:
        update.message.reply_text('Ничего не найдено, проверьте запрос.')
    return CHOOSING


def get_id_movie_TMDB(bot, update, user_data):
    movie_url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US",
        "query": user_data,
        "page": 1,
        "include_adult": "false"
    }
    result = requests.get(movie_url, params=params)
    id_movie_TMBD = result.json()
    return id_movie_TMBD


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
                           MessageHandler(Filters.text, search_actor,
                                          pass_user_data=True)],

            SEARCH_MOVIE: [RegexHandler('^(Отмена)$', back_to_menu,
                                        pass_user_data=True),
                           MessageHandler(Filters.text, get_id_movie,
                                          pass_user_data=True)],
        },

        fallbacks=[RegexHandler('^(Отмена)$', back_to_menu,
                                pass_user_data=True)]

    )

    dp = moviebot.dispatcher
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, talk_to_me,
                                  pass_user_data=True))
    moviebot.start_polling()
    moviebot.idle()


if __name__ == "__main__":
    main()
