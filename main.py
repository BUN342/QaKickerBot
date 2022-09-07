from cmath import nan
import time
import psycopg2
from collections import defaultdict
import telebot
from datetime import datetime, timedelta
from telebot import types
import threading


#TOKEN="5637357018:AAGg4dNhspCsx4kmk8ryk5yQ9Sl8mWqvK_Y"
TOKEN="5732654013:AAEs3Ke5uPUMiZBUk03DitDVVmteGiVENEE"
bot = telebot.TeleBot(TOKEN)
 
chats = {}
isStartPressed = False
isAnekdot = False
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
    # bot.send_message(message.chat.id, '@Yuriy')
    # bot.send_sticker(message.chat.id, 'CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE')
    test_timer(message, seconds_left)




@bot.message_handler(commands=['start'])
def start(message):
    global isStartPressed
    if(isStartPressed is True):
        bot.send_message(message.chat.id, "Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.", reply_markup=gen_markup())
        #bot.send_message(message.chat.id, 'Бот уже работает, тебе заняться нечем?')
        return
    
    isStartPressed = True

    now_chat = chat.Chat(conn)
    global chats
    chats[message.chat.id] = now_chat
    #bot.send_message(message.chat.id, 'Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.')    

    e1 = threading.Event()
    t1 = threading.Thread(target=test_timer, args=(message,1800))
    t1.start()
    e1.set()

    bot.send_message(message.chat.id, "Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.", reply_markup=gen_markup())

@bot.message_handler(commands=['help'])
def help(message):
    global isStartPressed
    if(isStartPressed is False):
        bot.send_message(message.chat.id, 'Напишите /start')
        return

    bot.send_message(message.chat.id, 'Вот, что я могу:\n', reply_markup=gen_markup())

@bot.message_handler(regexp="\w*\s*ф\w*\s*у\w*\s*т\w*\s*б\w*\s*о\w*\s*л")
def footballMsg(message):
     chat_id =  message.chat.id
     bot.send_message(chat_id, "Ага, я что-то услышал про футбол...\nРегайся на на игру командой /game")

@bot.message_handler(regexp="\w*\s*f\w*\s*o\w*\s*o\w*\s*t\w*\s*b\w*\s*a\w*\s*l\w*\s*l")
def footballMsg(message):
     chat_id =  message.chat.id
     bot.send_message(chat_id, "Ага, я что-то услышал про футбол...\nРегайся на на игру командой /game")

# @bot.message_handler(content_types=["sticker"])
# def handle_sticker(message):
#      bot.send_sticker(message.chat.id, 'CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global isAnekdot

    global isStartPressed
    if(isStartPressed is False):
        bot.send_message(call.message.chat.id, 'Напишите /start')
        return
    message = call.message
    global chats
    key = call.message.chat.id
    if(key not in chats):
        now_chat = chat.Chat(conn)
        chats[key] = now_chat
    else: 
        now_chat = chats[key]

    if call.data == "mystat": 
        bot.send_message(call.message.chat.id, call.from_user.first_name + ', твой ранг - %s. Давай поднажми, осталось совсем немного до нового ранга.' % now_chat.getMe(call.from_user.first_name))
        #bot.send_message(message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())
    elif call.data == "allstat":
        bot.send_message(call.message.chat.id, now_chat.getAll())
        #bot.send_message(message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())
    elif call.data == "create_game":
        createGameFunction(now_chat, call, call.from_user.first_name)
    elif call.data == "top_joke":
        if(isAnekdot is True):
            bot.answer_callback_query(call.id, "На сегодня анекдоты закончились.")
            return
        isAnekdot = True
        getJokeFunction(call, now_chat)
        
    elif call.data == "game_start":
        startGame(now_chat, call, call.from_user.first_name)
    elif call.data == "game_stop":
        stopGame(now_chat, call, call.from_user.first_name)
    elif call.data == "write_to_a_game":
        writeOnAGame(now_chat, call, call.from_user.first_name)
    elif call.data == "win_game":
        winGame(now_chat, call, call.from_user.first_name)
    elif call.data == "false_game":
        loseGame(now_chat, call, call.from_user.first_name)
    elif call.data == "top_anekdot":
        if(isAnekdot is True):
            bot.answer_callback_query(call.id, "На сегодня анекдоты закончились.")
            return

        isAnekdot = True
        getAnektod(call, now_chat)

    bot.answer_callback_query(call.id, "")

@bot.message_handler(regexp="\/\w+[@\w]*")
def handle_text(message):
    global isStartPressed
    if(isStartPressed is False):
        bot.send_message(message.chat.id, 'Напишите /start')
        return

    text = message.text.lower()
    chat_id =  message.chat.id
    
    global chats
    key = chat_id
    global now_chat
    if(key not in chats):
        now_chat = chat.Chat(conn)
        chats[key] = now_chat
    else: 
        now_chat = chats[key]

bot.polling(none_stop=True, interval=0)