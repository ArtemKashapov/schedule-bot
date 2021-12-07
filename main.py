import telebot
import config
from db_utils import Database

from threading import Thread
import time, random, datetime, math


bot = telebot.TeleBot(config.TOKEN)
db = Database()
week_number = 1
status = True

schedule = {
    1: {
        0:{
            1:['None', ''],
            2:['None', ''],
            3:['Философия', 'https://bbb.ssau.ru/b/vyz-6vv-phz'],
            4:['Технологии программирования', 'https://bbb1.ssau.ru/b/tq6-zn2-77p'],
            5:['Численные методы математической физики', 'https://bbb.ssau.ru/b/vvf-wqj-6cs-vfq'],
            6:['Теория цифровой обработки сигналов и изображений', 'https://bbb.ssau.ru/b/wyh-fo2-pmj-on8'],
        },
        1:{
            1:['None', ''],
            2:['None', ''],
            3:['Квантовая механика', 'https://bbb.ssau.ru/b/z3m-rli-v8j-rbi'],
            4:['Квантовая механика', 'https://bbb.ssau.ru/b/z3m-rli-v8j-rbi'],
            5:['Основы финансового учёта и анализа', 'https://bbb.ssau.ru/b/6tx-xea-r1y-eqw'],
            6:['Основы финансового учёта и анализа', 'https://bbb.ssau.ru/b/6tx-xea-r1y-eqw'],
        },
        2:{
            1:['Военная подготовка', 'Face-to-face'],
            2:['None', ''],
            3:['None', ''],
            4:['None', ''],
            5:['None', ''],
            6:['None', ''],
        },
        3:{
            1:['Иностранный язык(1)', 'https://bbb.ssau.ru/b/ef9-vuu-3aj'],
            2:['Иностранный язык(1)', 'https://bbb.ssau.ru/b/ef9-vuu-3aj'],
            3:['Теория цифровой обработки сигналов и изображений', 'https://bbb.ssau.ru/b/z3n-3rp-rkx'],
            4:['Численные методы математической физики', 'https://bbb.ssau.ru/b/vvf-wqj-6cs-vfq'],
            5:['None', ''],
            6:['None', ''],
        },
        4:{
            1:['None', ''],
            2:['Иностранный язык(2)', 'https://bbb2.ssau.ru/b/6qa-7r3-rnz'],
            3:['Иностранный язык(2)', 'https://bbb2.ssau.ru/b/6qa-7r3-rnz'],
            4:['Нелинейная динамика', 'Mail.ru'],
            5:['Нелинейная динамика', 'Mail.ru'],
            6:['Основы финансового учёта и анализа', 'https://bbb.ssau.ru/b/6tx-xea-r1y-eqw'],
        },
    },
    2: {
        0:{
            1:['None', ''],
            2:['None', ''],
            3:['Философия', 'https://bbb.ssau.ru/b/vyz-6vv-phz'],
            4:['Технологии программирования', 'https://bbb1.ssau.ru/b/tq6-zn2-77p'],
            5:['Численные методы математической физики', 'https://bbb.ssau.ru/b/vvf-wqj-6cs-vfq'],
            6:['Теория цифровой обработки сигналов и изображений', 'https://bbb.ssau.ru/b/wyh-fo2-pmj-on8'],
        },
        1:{
            1:['None', ''],
            2:['None', ''],
            3:['Квантовая механика', 'https://bbb.ssau.ru/b/z3m-rli-v8j-rbi'],
            4:['Квантовая механика', 'https://bbb.ssau.ru/b/z3m-rli-v8j-rbi'],
            5:['Квантовая механика', 'https://bbb.ssau.ru/b/z3m-rli-v8j-rbi'],
            6:['Иностранный язык(2)', 'https://bbb2.ssau.ru/b/6qa-7r3-rnz'],
        },
        2:{
            1:['Военная подготовка', 'Face-to-face'],
            2:['None', ''],
            3:['None', ''],
            4:['None', ''],
            5:['None', ''],
            6:['None', ''],
        },
        3:{
            1:['None', ''],
            2:['None', ''],
            3:['Теория цифровой обработки сигналов и изображений', 'https://bbb.ssau.ru/b/z3n-3rp-rkx'],
            4:['Иностранный язык(1)', 'https://bbb.ssau.ru/b/ef9-vuu-3aj'],
            5:['Иностранный язык(1)', 'https://bbb.ssau.ru/b/ef9-vuu-3aj'],
            6:['None', ''],
        },
        4:{
            1:['None', ''],
            2:['Иностранный язык(2)', 'https://bbb2.ssau.ru/b/6qa-7r3-rnz'],
            3:['Нелинейная динамика', 'Mail.ru'],
            4:['Нелинейная динамика', 'Mail.ru'],
            5:['Квантовая механика', 'https://bbb.ssau.ru/b/z3m-rli-v8j-rbi'],
            6:['None', ''],
        },
    },
}

start_time = {
    1: 8 * 60 - 2,
    2: 9 * 60 + 45 - 2,
    3: 11 * 60 + 30 - 2,
    4: 13 * 60 + 30 - 2,
    5: 15 * 60 + 15 - 2,
    6: 17 * 60 - 2,
}


@bot.message_handler(content_types=['text'])
def start(message):
    try:
        db.insert_user(message.from_user.id)
        bot.send_message(message.from_user.id, 'Теперь ты будешь получать уведомления о начале занятий!')
    except:
        bot.send_message(message.from_user.id, 'Ты уже получаешь уведомления о расписании ;-)')


def func1():
    bot.polling()

def func2():
    
    while True:
        users = [int(item[0]) for item in db.get_all()]

        for user in users:
            bot.send_message(user, get_message())
        
        delay = get_delay()
        time.sleep(delay)



def get_delay():
    hour = datetime.datetime.now().hour
    day_of_week = datetime.datetime.today().weekday()
    if (day_of_week > 4) or (day_of_week > 4 and hour > 17):
        return 3600 + random.random()
    else:
        return 300 + random.random()

def get_message():

    now = datetime.datetime.now().hour * 60 + datetime.datetime.now().minute
    day_of_week = datetime.datetime.today().weekday()

    error = 5

    for key, value in start_time.items():
        if math.fabs(value - now) <= error:
            title = schedule[week_number][day_of_week][key][0]
            link = schedule[week_number][day_of_week][key][1]
            return f'Не забудь про {title}, можно подключиться по {link}'


if __name__ == '__main__':
    Thread(target = func1).start()
    Thread(target = func2).start()