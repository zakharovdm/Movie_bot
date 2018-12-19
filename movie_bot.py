import greeting
import settings

from telegram.ext import Updater, CommandHandler, RegexHandler 
from telegram import ReplyKeyboardMarkup






def greet_user(bot,update):
	ave_text = 'Привет {}! {} '.format(update.message.chat.first_name, greeting.greet_text) 
	menu_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера']])
	update.message.reply_text(ave_text, reply_markup = menu_keyboard)

def get_actor_by_name(bot, update):
	text = 'test'
	update.message.reply_text(text)


def main():
	moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

	dp = moviebot.dispatcher
	dp.add_handler(CommandHandler('start', greet_user))
	dp.add_handler(CommandHandler('get_actor', get_actor_by_name))
	dp.add_handler(RegexHandler('^(Поиск актера)$', get_actor_by_name))

	

	moviebot.start_polling()
	moviebot.idle()


if __name__ =="__main__": 
    main() 
