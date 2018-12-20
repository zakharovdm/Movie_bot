import greeting
import settings

from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, MessageHandler, 
                         Filters  

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove



CHOICE, SEARCH_ACTOR, SEARCH_MOVIE = range (3)


def greet_user(bot,update):                              
	ave_text = 'Привет {}! {} '.format(update.message.chat.first_name, greeting.greet_text) 
	menu_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера']])
	update.message.reply_text(ave_text, reply_markup = menu_keyboard)

def get_actor_by_name(bot, update):                                 
	text = 'test_actor'
	update.message.reply_text(text)

def get_get_movie_by_name(bot, update):
	text = 'test_film'
	update.message.reply_text(text)


def main():
	moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

	conv_handler = ConversationHandler(
		    entry_points = [CommandHandler('start', greet_user)], 

		    states ={
		    	CHOICE: [RegexHandler('^(Поиск актера)$', get_actor_by_name),
		    			RegexHandler('^(Поиск фильма)$', get_movie_by_name)],

		    	SEARCH_ACTOR: [MessageHandler(Filters.text, get_actor_by_name)],

		    	SEARCH_MOVIE: [MessageHandler(Filters.text, get_movie_by_name)], 

		    	},

		    fallbacks = [CommandHandler ('back_to_menu', back_to_menu)]	 
			
				)

	dp = moviebot.dispatcher
	dp.add_handler(CommandHandler('start', greet_user))
	dp.add_handler(CommandHandler('get_actor', get_actor_by_name))
	dp.add_handler(CommandHandler('get_movie', get_movie_by_name))
	dp.add_handler(conv_handler)

	

	moviebot.start_polling()
	moviebot.idle()


if __name__ =="__main__": 
    main() 
