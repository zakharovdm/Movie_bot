import handlers
import requests


def reply_actor_biography(bot, update, user_data, TMDB_actor_id):
    bio = user_data["biography"]
    update.message.reply_text(f"""Биография: {bio}""")


def reply_box_office(bot, update, user_data, TMDB_id):
    box_office = user_data
    update.message.reply_text(f"""Сборы по миру: {box_office} $""")
    update.message.reply_text("Что еще ты хочешь найти? Выбирай.")
    return handlers.CHOOSING


def reply_actor_birth_date(bot, update, user_data, TMDB_actor_id):
    birth_date_actor = user_data["birthday"]
    update.message.reply_text(f"""Дата рождения: {birth_date_actor}""")
    reply_actor_biography(bot, update, user_data, TMDB_actor_id)


def reply_actor_photo(bot, update, user_data, TMDB_actor_id):
    """Выдача фотографии актера.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    actor_id = TMDB_actor_id
    url = f"""https://api.themoviedb.org/3/person/{actor_id}"""
    params = {
        "api_key": "bb46ace44fb728f5f7575bf3b4531ad3",
        "language": "en-US"
    }
    result = requests.get(url, params=params)
    info_actor_json = result.json()
    photo_file = info_actor_json["profile_path"]
    photo_url = f"""https://image.tmdb.org/t/p/w500{photo_file}"""
    bot.send_photo(chat_id=update.message.chat.id, photo=photo_url)
    user_data = info_actor_json
    reply_actor_birth_date(bot, update, user_data, TMDB_actor_id)


def reply_release_date(bot, update, user_data, TMDB_id):
    """Выдача даты выпуска.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    release = info_movie['original air date']
    update.message.reply_text(f"Дата выхода: {release}")


def reply_main_roles(bot, update, user_data, TMDB_id):
    """Выдача актеров в главных ролях фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    name_actors = []
    for actor in info_movie['cast'][:6]:
        name_actors.append(f"""{actor['name']} в роли {actor.currentRole}""")
    main_actors = '\n'.join(name_actors)
    update.message.reply_text(f"""В главных ролях: {main_actors}""")
    reply_release_date(bot, update, user_data, TMDB_id)


def reply_directors(bot, update, user_data, TMDB_id):
    """Выдача режиссеров фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    directors_info = info_movie['director'][0:]
    name_director = []
    for directors in directors_info:
        name_director.append(directors['name'])
    producers = ', '.join(name_director)
    update.message.reply_text(f"Режиссеры: {producers}")
    reply_main_roles(bot, update, user_data, TMDB_id)


def reply_description(bot, update, user_data, TMDB_id):
    """Выдает краткое описание фильма.

    Args:
        bot: Объект, который передается обработчикам.
        update: Сообщение которое пришло от Telegramm.
        user_data: Хранит данные от пользователя.

    """
    info_movie = user_data
    parts = info_movie['plot'][0].split('::')
    short_description = parts[0]
    update.message.reply_text(short_description)
    reply_directors(bot, update, user_data, TMDB_id)


if __name__ == "__main__":
    handlers.main()
