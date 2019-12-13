import greeting
import logging
import handlers
from telegram import ReplyKeyboardMarkup, KeyboardButton


def menu_keyboard():
    get_location = KeyboardButton('Определить месторасположение',
                                  request_location=True)
    film_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера'],
                                         ['Отмена', get_location]
                                         ], resize_keyboard=True
                                        )
    return film_keyboard


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

    return handlers.CHOOSING


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

    return handlers.ConversationHandler.END
