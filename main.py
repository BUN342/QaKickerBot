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
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    # bot.send_message(message.chat.id, '@Yuriy')
    # bot.send_sticker(message.chat.id, 'CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE')
    test_timer(message, seconds_left)

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Создать игру", callback_data="create_game"),
                               InlineKeyboardButton("Вывести общую статистику", callback_data="allstat"),
                               InlineKeyboardButton("Вывести мою статистику", callback_data="mystat"),
                               InlineKeyboardButton("Шутка дня", callback_data="top_joke"))
    return markup

def getJokeFunction(message):
    joke = pyjokes.get_joke()
    bot.send_message(message.chat.id,joke)
    bot.send_message(message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())

def createGameFunction(now_chat, message):
    isGame = now_chat.createGame(message.from_user.first_name)
    if(isGame is False):
        bot.send_message(message.chat.id, 'Игру уже кто-то начал.\nЗаверши предыдущую, прежде чем начать новую.\nКомианда /gamestop')
        return

    bot.send_message(message.chat.id, 'Так, так, так.. Кто это тут у нас хочет начать игру?\nДавайте поможем %s собрать участников, пиши /me, если хочешь присоединиться к игре.' % message.from_user.first_name)

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
        bot.send_message(message.chat.id, 'Запусти бота, чорт')
        return

    bot.send_message(message.chat.id, 'Вот, чем я могу помочь тебе:\n /reg - регистрация в рейтинге;\n /game - начать игру;\n /allstats - общая статистика;\n /mystat - персональная статистика\n /gamestart - начать игру, если нашлось 4 игрока;\n /gamestop - прервать игру, если все воркают и не набралось игроков или кикер занят;\n /win - это пишет создатель игры, если его команда победила;\n /lose - это пишет создатель игры, если его команда проиграла;\n /getjoke - получить хохму на не нашем языке')

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
    message = call.message

    now_chat = chats[message.chat.id]

    if call.data == "mystat": 
        bot.send_message(call.message.chat.id, call.from_user.first_name + ', твой ранг - %s. Давай поднажми, осталось совсем немного до нового ранга.' % now_chat.getMe(call.from_user.first_name))
        bot.send_message(message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())
    elif call.data == "allstat":
        bot.send_message(call.message.chat.id, now_chat.getAll())
        bot.send_message(message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())
    elif call.data == "create_game":
        createGameFunction(now_chat, call.message)
    elif call.data == "top_joke":
        getJokeFunction(call.message)

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
        createGameFunction(message)
        
    elif text == "/me" or text == "/me@qakickerratingbot":
        isMe = now_chat.writeUserToGame(message.from_user.first_name)
        if(isMe == 1):
            bot.send_message(chat_id, '%s, в данный момент идёт игра, жди.' % message.from_user.first_name)
        elif(isMe == 2):
            bot.send_message(chat_id, 'Игроков уже достаточно.')
        elif(isMe == 3):
            bot.send_message(chat_id, 'Ты уже в игре, дай другим записаться.')
        elif(isMe == 4):
            bot.send_message(chat_id, 'И куда ты регаться пытаешься?')
        else:
            #bot.send_message(chat_id, 'Все готовы?\nПишите /gamestart, чтобы начать игру.\nИли /gamestop, если хотите отменить игру.')
            bot.send_message(chat_id, '%s, ты записался. \nЕсли все готовы, то пишите /gamestart, чтобы начать игру.\nИли /gamestop, если хотите отменить игру.' % message.from_user.first_name)

    elif text == "/gamestart" or text == "/gamestart@qakickerratingbot":
        isGameStart = now_chat.gameStart(message.from_user.first_name)
        if(isGameStart == 0):
            bot.send_message(chat_id, 'Ты не создатель игры, иди лесом.')
            return
        elif(isGameStart == 1):
            bot.send_message(chat_id, 'Слишком мало игроков для игры.')
            return
        elif(isGameStart == 2):
            bot.send_message(chat_id, 'Идёт игра, жди очереди.')
            return

        players = isGameStart

        teams = "Наши команды:\n"
        team = list(players.items())

        if(len(team) == 2):
            teams += team[0][0] + " и " + team[1][0]
        elif(len(team) == 4):
            team = list(players.items())
            teams += team[0][0] + " и " + team[1][0] + ",\n" + team[2][0] + " и " + team[3][0]
            
        bot.send_message(chat_id,teams + "\nИгра началась!")
    elif text == "/gamestop" or text == "/gamestop@qakickerratingbot":
        isGameStop = now_chat.gameStop(message.from_user.first_name)
        if(isGameStop == 0):
            bot.send_message(chat_id, 'Ты не создатель игры, иди лесом.')
            return
        elif (isGameStop == 1):
            bot.send_message(chat_id, 'Игра даже не началась, отменять нечего.')
            return
        elif (isGameStop == 2):
            bot.send_message(chat_id, 'Отменять нечего.')
        elif (isGameStop == 3):
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
        getJokeFunction(message)
# Запускаем бота
bot.polling(none_stop=True, interval=0)
