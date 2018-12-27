import greeting
import imdb
import settings
import logging

from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, MessageHandler, Filters  

from telegram import ReplyKeyboardMarkup


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='movie_bot.log'
                    )



CHOOSING, SEARCH_ACTOR, SEARCH_MOVIE = range (3)

def back_to_menu(bot, update, user_data):
	update.message.reply_text('пока')

	return ConversationHandler.END


def greet_user(bot,update, user_data):                              
	ave_text = 'Привет {}! {} '.format(update.message.chat.first_name, greeting.greet_text) 
	menu_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера'],
											         ['Отмена']])
	logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text)
	print(("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                 update.message.chat.id, update.message.text))
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
	id_actor = actor[0].personID
	info_actor = ia.get_person(id_actor)
	update.message.reply_text(info_actor['bio']) 

	
	return CHOOSING

def search_movie(bot, update, user_data):
	ia = imdb.IMDb()
	user_query = update.message.text
	user_data['movie'] = user_query
	movie = ia.search_movie(user_query)
	id_movie = movie[0].movieID
	info_movie = ia.get_movie(id_movie)
	update.message.reply_text(info_movie['plot'])

	
	return CHOOSING

	

def main():
	moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

	logging.info('Бот запускается')
	print('Бот запускается') 

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
