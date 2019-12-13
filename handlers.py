import logging
import settings
from telegram.ext import (Updater, CommandHandler, RegexHandler,
                          ConversationHandler, MessageHandler, Filters)
from menu import greet_user, talk_to_me, back_to_menu
from informations import (get_actor_by_name, get_movie_by_name,
                          get_actor_TMDB_id, get_movie_TMDB_id, get_location)


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='movie_bot.log'
                    )


CHOOSING, SEARCH_ACTOR, SEARCH_MOVIE = range(3)

moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)


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


def main():

    dp = moviebot.dispatcher
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.location, get_location,
                                  pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me,
                                  pass_user_data=True))
    moviebot.start_polling()
    moviebot.idle()
