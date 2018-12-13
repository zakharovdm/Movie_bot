from telegram.ext import Updater 
import settings

def main():
	moviebot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

	

	moviebot.start_polling()
	moviebot.idle()


if __name__ =="__main__": 
    main() 
