import greeting
import settings

from telegram.ext import Updater, CommandHandler 
from telegram import ReplyKeyboardMarkup






def greet_user(bot,update):
	ave_text = 'Привет {}! {} '.format(update.message.chat.first_name, greeting.greet_text) 
	menu_keyboard = ReplyKeyboardMarkup([['Поиск фильма', 'Поиск актера']])
	update.message.reply_text(ave_text, reply_markup = menu_keyboard)


def main():
	moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

	dp = moviebot.dispatcher
	dp.add_handler(CommandHandler('start', greet_user))

	

	moviebot.start_polling()
	moviebot.idle()


if __name__ =="__main__": 
    main() 
