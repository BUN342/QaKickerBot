from cmath import nan
import time
import psycopg2
from collections import defaultdict
import telebot
from datetime import datetime, timedelta
from telebot import types
import threading
import chat
import registration

TOKEN="5637357018:AAGg4dNhspCsx4kmk8ryk5yQ9Sl8mWqvK_Y"
#TOKEN="5732654013:AAEs3Ke5uPUMiZBUk03DitDVVmteGiVENEE"
bot = telebot.TeleBot(TOKEN)
 
chats = {}
isStartPressed = False
user = 'mdriysdmzxohga'
password = 'd5016c9242569d17b84950f4d0cb9ba3be135fbdff7d89e09f96785d5845e9a2'
db_name = 'dbf5g5orv48dsr'
host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com'
port = 5432
rank = "TRAINEE I"
POOL_TIME_FOR_GAME=5

conn = psycopg2.connect(dbname=db_name, user=user, 
                        password=password, host=host)

def test_timer(message, seconds_left):
    total_seconds = seconds_left
    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1

    global chats
    chats = {}
    bot.send_message(message.chat.id, 'Расовая чистка произведена')
    test_timer(message, seconds_left)

@bot.message_handler(commands=['start'])
def start(message):
    global isStartPressed
    if(isStartPressed is True):
        bot.send_message(message.chat.id, 'Бот уже работает, тебе заняться нечем?')
        return
    
    isStartPressed = True

    now_chat = chat.Chat(conn)
    global chats
    chats[message.chat.id] = now_chat

    bot.send_message(message.chat.id, 'Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.')

    e1 = threading.Event()
    t1 = threading.Thread(target=test_timer, args=(message,300))
    t1.start()
    e1.set()

@bot.message_handler(commands=['help'])
def help(message):
    global isStartPressed
    if(isStartPressed is False):
        bot.send_message(message.chat.id, 'Запусти бота, чорт')
        return

    bot.send_message(message.chat.id, 'Вот, чем я могу помочь тебе:\n /reg - регистрация\n /game - начать игру\n /allstats - общая статистика\n /mystat - твоя статистика')

@bot.message_handler(regexp="\w*\s*ф\w*\s*у\w*\s*т\w*\s*б\w*\s*о\w*\s*л")
def footballMsg(message):
     chat_id =  message.chat.id
     bot.send_message(chat_id, "Ага, я что-то услышал про футбол...\nРегайся на на игру командой /game")

@bot.message_handler(regexp="\w*\s*f\w*\s*o\w*\s*o\w*\s*t\w*\s*b\w*\s*a\w*\s*l\w*\s*l")
def footballMsg(message):
     chat_id =  message.chat.id
     bot.send_message(chat_id, "Ага, я что-то услышал про футбол...\nРегайся на на игру командой /game")

@bot.message_handler(regexp="\/\w+[@\w]*")
def handle_text(message):
    global isStartPressed
    if(isStartPressed is False):
        bot.send_message(message.chat.id, 'Запусти бота, чорт')
        return

    text = message.text.lower()
    chat_id =  message.chat.id
    
    global chats
    key = chat_id
    global now_chat
    if(key not in chats):
        now_chat = chat.Chat(conn)
    else: 
        now_chat = chats[key]

    isReg = now_chat.registration(message.from_user.first_name)

    if (text == "/reg" or text == "/reg@qakickerratingbot"):
        if(isReg is True):
            bot.send_message(chat_id, message.from_user.first_name + ', ты зарегался и сейчас у тебя TRAINEE I ранг.\nДумал все так просто будет?')
        else:
            bot.send_message(chat_id, message.from_user.first_name + ', ты уже зарегался')
    elif text == "/game" or text == "/game@qakickerratingbot":
        isGame = now_chat.createGame(message.from_user.first_name)
        if(isGame is False):
            bot.send_message(chat_id, 'Игру уже кто-то начал.\nЗаверши предыдущую, прежде чем начать новую.\nКомианда /gamestop')

        bot.send_message(chat_id, 'Так, так, так.. Кто это тут у нас хочет начать игру?\nДавайте поможем %s собрать участников, пиши /me, если хочешь присоединиться к игре.' % message.from_user.first_name)
        
    elif text == "/me" or text == "/me@qakickerratingbot":
        
        bot.send_message(chat_id, '%s, ты уже записался на игру, жди начала' % message.from_user.first_name)

        bot.send_message(chat_id, 'Данных нет!')

        bot.send_message(chat_id, 'Игр нет!')

        bot.send_message(chat_id, 'Все готовы?\nПишите /gamestart, чтобы начать игру.\nИли /gamestop, если хотите отменить игру')

            
    elif text == "/gamestart" or text == "/gamestart@qakickerratingbot":
            bot.send_message(chat_id, 'Игра началась!\n*дальнейший функционал будет готов в следующем релизе*')
    elif text == "/gamestop" or text == "/gamestop@qakickerratingbot":
            bot.send_message(chat_id, 'Чё, обоссались?\n*дальнейший функционал будет готов в следующем релизе*')
    elif text == "/mystat" or text == "/mystat@qakickerratingbot": 
        bot.send_message(chat_id, message.from_user.first_name + ', твой ранг - %s. Давай поднажми, осталось совсем немного до нового ранга.' % now_chat.getMe(message.from_user.first_name))
    elif text == "/allstats" or text == "/allstats@qakickerratingbot":
        bot.send_message(chat_id, now_chat.getAll())

# Запускаем бота
bot.polling(none_stop=True, interval=0)