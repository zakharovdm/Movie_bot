import greeting
import settings

from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, MessageHandler, Filters  

from telegram import ReplyKeyboardMarkup

import imdb



CHOOSING, SEARCH_ACTOR, SEARCH_MOVIE = range (3)

def back_to_menu(bot, update, user_data):
	update.message.reply_text('пока')

	return ConversationHandler.END


def greet_user(bot,update, user_data):                              
	ave_text = 'Привет {}! {} '.format(update.message.chat.first_name, greeting.greet_text) 
	menu_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера'],
											         ['Отмена']])
	update.message.reply_text(ave_text, reply_markup = menu_keyboard)

	return CHOOSING

def get_actor_by_name(bot, update, user_data):                                 
	question = 'Какого актера найти?'
	update.message.reply_text(question)
	return SEARCH_ACTOR


	
def get_movie_by_name(bot, update, user_data):
	question = 'Какой фильм найти?'
	update.message.reply_text(question)
	return SEARCH_MOVIE
 
	
def search_actor(bot, update, user_data):
	ia = imdb.IMDb()
	user_query = update.message.text 
	user_data['actor'] = user_query
	actor = ia.search_person(user_query) 
	update.message.reply_text(actor[0]) 

	
	return CHOOSING

def search_movie(bot, update, user_data):
	text = update.message.text
	user_data['movie'] = text
	update.message.reply_text('Ищем {}, потом здесь будет результат поиска'.format(text.title()))

	
	return CHOOSING

	

def main():
	moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

	conv_handler = ConversationHandler(
		    entry_points = [CommandHandler('start', greet_user,pass_user_data = True),
		    RegexHandler('^(Поиск актера)$', get_actor_by_name, pass_user_data = True),
		    RegexHandler('^(Поиск фильма)$', get_movie_by_name, pass_user_data = True)],

		    states = {
		    	CHOOSING: [RegexHandler('^(Поиск актера)$', get_actor_by_name, pass_user_data = True), 
		    			RegexHandler('^(Поиск фильма)$', get_movie_by_name, pass_user_data = True)],

		    	SEARCH_ACTOR: [RegexHandler('^(Отмена)$', back_to_menu, pass_user_data = True),
		    					MessageHandler(Filters.text, search_actor, pass_user_data = True)],

		    	SEARCH_MOVIE: [RegexHandler('^(Отмена)$', back_to_menu, pass_user_data = True),
		    					MessageHandler(Filters.text, search_movie, pass_user_data = True)], 

		    	},

		    fallbacks = [RegexHandler('^(Отмена)$', back_to_menu, pass_user_data = True)]	

		    )

	dp = moviebot.dispatcher
	dp.add_handler(conv_handler)
	

	moviebot.start_polling()
	moviebot.idle()


if __name__ =="__main__": 
    main() 
