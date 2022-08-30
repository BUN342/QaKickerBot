from cmath import nan
import time
import psycopg2
from collections import defaultdict
import telebot
from datetime import datetime, timedelta
from telebot import types
import threading
import chat
import pyjokes
from googletrans import Translator

#TOKEN="5637357018:AAGg4dNhspCsx4kmk8ryk5yQ9Sl8mWqvK_Y"
TOKEN="5732654013:AAEs3Ke5uPUMiZBUk03DitDVVmteGiVENEE"
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
    test_timer(message, seconds_left)

def joke_timer(message, seconds_left):
    total_seconds = seconds_left
    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1
    joke = pyjokes.get_joke()
    translator = Translator()
    joke_result = translator.translate(joke, dest='ru')
    bot.send_message(message.chat.id,joke_result.text)
    joke_timer(message, seconds_left)

def getJoke(message):
    joke = pyjokes.get_joke()
    translator = Translator()
    joke_result = translator.translate(joke, dest='ru')
    bot.send_message(message.chat.id,joke_result.text)

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
    e2 = threading.Event()
    
    t1 = threading.Thread(target=test_timer, args=(message,300))
    t2 = threading.Thread(target=test_timer, args=(message,1800))

    t1.start()
    t2.start()

    e1.set()
    e2.set()

@bot.message_handler(commands=['help'])
def help(message):
    global isStartPressed
    if(isStartPressed is False):
        bot.send_message(message.chat.id, 'Запусти бота, чорт')
        return

    bot.send_message(message.chat.id, 'Вот, чем я могу помочь тебе:\n /reg - регистрация;\n /game - начать игру;\n /allstats - общая статистика;\n /mystat - твоя статистика.')

@bot.message_handler(regexp="\w*\s*ф\w*\s*у\w*\s*т\w*\s*б\w*\s*о\w*\s*л")
def footballMsg(message):
     chat_id =  message.chat.id
     bot.send_message(chat_id, "Ага, я что-то услышал про футбол...\nРегайся на на игру командой /game")

@bot.message_handler(regexp="\w*\s*f\w*\s*o\w*\s*o\w*\s*t\w*\s*b\w*\s*a\w*\s*l\w*\s*l")
def footballMsg(message):
     chat_id =  message.chat.id
     bot.send_message(chat_id, "Ага, я что-то услышал про футбол...\nРегайся на на игру командой /game")

@bot.message_handler(content_types=["sticker"])
def handle_sticker(message):
     bot.send_sticker(message.chat.id, 'CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE')
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
        chats[key] = now_chat
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
            return

        bot.send_message(chat_id, 'Так, так, так.. Кто это тут у нас хочет начать игру?\nДавайте поможем %s собрать участников, пиши /me, если хочешь присоединиться к игре.' % message.from_user.first_name)
        
    elif text == "/me" or text == "/me@qakickerratingbot":
        isMe = now_chat.writeUserToGame(message.from_user.first_name)
        if(isMe == 1):
            bot.send_message(chat_id, '%s, в данный момент идёт игра, жди.' % message.from_user.first_name)
        elif(isMe == 2):
            bot.send_message(chat_id, 'Игроков уже достаточно.')
        elif(isMe == 3):
            bot.send_message(chat_id, 'Ты уже в игре, дай другим записаться.')
        else:
            #bot.send_message(chat_id, 'Все готовы?\nПишите /gamestart, чтобы начать игру.\nИли /gamestop, если хотите отменить игру.')
            bot.send_message(chat_id, '%s, ты записался. \nЕсли все готовы, то пишите /gamestart, чтобы начать игру.\nИли /gamestop, если хотите отменить игру.' % message.from_user.first_name)

    elif text == "/gamestart" or text == "/gamestart@qakickerratingbot":
        isGameStart = now_chat.gameStart()
        if(isGameStart == 1):
            bot.send_message(chat_id, 'Слишком мало игроков для игры.')
            return
        elif(isGameStart == 2):
            bot.send_message(chat_id, 'Идёт игра, жди очереди.')
            return
        bot.send_message(chat_id, 'Игра началась!')
    elif text == "/gamestop" or text == "/gamestop@qakickerratingbot":
        isGameStop = now_chat.gameStop()
        if(isGameStop is False):
            bot.send_message(chat_id, 'Игра даже не началась, отменять нечего.')
            return
        bot.send_message(chat_id, 'Игра отменена.')
    elif text == "/win" or text == "/win@qakickerratingbot":
        isResult = now_chat.writeResult(True, message.from_user.first_name)
        if(isResult == 0):
            bot.send_message(chat_id, 'Ты не создатель игры, иди лесом.')
            return
        elif(isResult == 1):
            bot.send_message(chat_id, 'Игра даже не началась.')
            return
        else:
            bot.send_message(chat_id, 'Результаты зафиксированы.')
    elif text == "/lose" or text == "/lose@qakickerratingbot":
        isResult = now_chat.writeResult(False, message.from_user.first_name)
        if(isResult == 0):
            bot.send_message(chat_id, 'Ты не создатель игры, иди лесом.')
            return
        elif(isResult == 1):
            bot.send_message(chat_id, 'Игра даже не началась.')
            return
        else:
            bot.send_message(chat_id, 'Результаты зафиксированы.')
    elif text == "/mystat" or text == "/mystat@qakickerratingbot": 
        bot.send_message(chat_id, message.from_user.first_name + ', твой ранг - %s. Давай поднажми, осталось совсем немного до нового ранга.' % now_chat.getMe(message.from_user.first_name))
    elif text == "/allstats" or text == "/allstats@qakickerratingbot":
        bot.send_message(chat_id, now_chat.getAll())
    elif text == "/getjoke" or text == "/getjoke@qakickerratingbot":
        getJoke(message)
# Запускаем бота
bot.polling(none_stop=True, interval=0)