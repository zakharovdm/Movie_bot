import greeting
import imdb
import settings
import logging

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
    menu_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера'],
                                         ['Отмена']
                                         ]
                                        )
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
    update.message.reply_text(ave_text, reply_markup=menu_keyboard)

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


def search_movie(bot, update, user_data):
    """Обращается к базе данных IMDb
    для поиска и выдачи информации о фильме.

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
        info_movie = ia.get_movie(id_movie)
        message_length = 0
        for list in info_movie['plot']:
            message_length += len(list)
        if message_length > 4096:
            part_info_movie = info_movie['plot']
            part_one = part_info_movie[:len(part_info_movie) // 2]
            part_two = part_info_movie[len(part_info_movie) // 2:]
            update.message.reply_text(part_one)
            update.message.reply_text(part_two)
        else:
            update.message.reply_text(info_movie['plot'])

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
    except IndexError:
        update.message.reply_text('Ничего не найдено, проверьте запрос.')
    return CHOOSING


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
                           MessageHandler(Filters.text, search_movie,
                                          pass_user_data=True)],
        },

        fallbacks=[RegexHandler('^(Отмена)$', back_to_menu,
                                pass_user_data=True)]

    )

    dp = moviebot.dispatcher
    dp.add_handler(conv_handler)
    moviebot.start_polling()
    moviebot.idle()


if __name__ == "__main__":
    main()
