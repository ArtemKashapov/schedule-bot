import telebot
import config
from db_utils import Database


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def start(message):

    # print(message)
    # print(message.from_user.id)

    try:
        db = Database()
        db.insert_user(message.from_user.id)
        bot.send_message(message.from_user.id, 'Ты записан в бд')
    except:
        bot.send_message(message.from_user.id, 'Ты не записан в бд')
    finally:
        db.close_all()




bot.polling(non_stop=True)
