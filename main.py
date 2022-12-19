from cmath import nan
import time
import psycopg2
from collections import defaultdict
import telebot
from datetime import datetime, timedelta
from telebot import types
import threading
import chat
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


#TOKEN="5637357018:AAGg4dNhspCsx4kmk8ryk5yQ9Sl8mWqvK_Y"
TOKEN="5732654013:AAEs3Ke5uPUMiZBUk03DitDVVmteGiVENEE"
bot = telebot.TeleBot(TOKEN)
 
chats = {}
isStartPressed = False
user = 'tester'
password = '123123'
db_name = 'testdb'
host='172.28.2.54'
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
                               InlineKeyboardButton("Шутка дня", callback_data="top_joke"),
                               InlineKeyboardButton("Анекдот дня", callback_data="top_anekdot"))
    return markup

def game_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Начать игру", callback_data="game_start"),
                               InlineKeyboardButton("Отменить игру", callback_data="game_stop"),
                               InlineKeyboardButton("Записаться на игру", callback_data="write_to_a_game"),
                               InlineKeyboardButton("Моя команда победила", callback_data="win_game"),
                               InlineKeyboardButton("Моя команда проиграла", callback_data="false_game"))
    return markup    

def getJokeFunction(message, now_chat):
    bot.send_message(message.message.chat.id, now_chat.getHohma(1))
    #bot.send_message(message.message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())

def getAnektod(message, now_chat):
    anekdot = now_chat.getHohma(2)
    if(anekdot == -1):
         bot.answer_callback_query(message.id, "Анекдоты закончились")
    else:
        bot.send_message(message.message.chat.id, anekdot)

def createGameFunction(now_chat, message, from_who):
    isGame = now_chat.createGame(from_who)
    if(isGame is False):
        bot.answer_callback_query(message.id, 'Игру уже кто-то начал.\nЗаверши предыдущую, прежде чем начать новую.')
        return

    bot.send_message(message.message.chat.id, 'Так, так, так.. Кто это тут у нас хочет начать игру?\nДавайте поможем %s собрать участников.\nСейчас в 1/4 игроков в игре.' % from_who, reply_markup=game_markup())

def writeOnAGame(now_chat, message, from_who):
    isMe = now_chat.writeUserToGame(from_who)
    if(isMe == 1):
        bot.answer_callback_query(message.id, '%s, в данный момент идёт игра, жди.' % from_who)
    elif(isMe == 2):
        bot.answer_callback_query(message.id, '%s, игроков уже достаточно.' % from_who)
    elif(isMe == 3):
        bot.answer_callback_query(message.id, '%s, ты уже в игре, дай другим записаться.' % from_who)
    elif(isMe == 4):
        bot.answer_callback_query(message.id, '%s, и куда ты регаться пытаешься?' % from_who)
    else:
        keys = list(isMe.keys())
        bot.delete_message(message.message.chat.id, message.message.id)
        bot.send_message(message.message.chat.id, 'Так, так, так.. Кто это тут у нас хочет начать игру?\nДавайте поможем %s собрать участников.\nСейчас в %s/4 игроков в игре.' % (keys[0], len(isMe)), reply_markup=game_markup())
    
    
def startGame(now_chat, message, from_who):
    isGameStart = now_chat.gameStart(from_who)
    if(isGameStart == 0):
        bot.answer_callback_query(message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif(isGameStart == 1):
        bot.answer_callback_query(message.id, 'Слишком мало игроков для игры.')
        return
    elif(isGameStart == 2):
        bot.answer_callback_query(message.id, 'Идёт игра, жди очереди.')
        return
    elif(isGameStart == 3):
        bot.answer_callback_query(message.id, 'Ты не создатель игры, иди лесом.')
        return

    players = isGameStart

    teams = "Наши команды:\n"
    team = list(players.items())

    if(len(team) == 2):
        teams += team[0][0] + " vs " + team[1][0]
    elif(len(team) == 4):
        team = list(players.items())
        teams += team[0][0] + " и " + team[2][0] + "\nvs\n" + team[1][0] + " и " + team[3][0]
            
    bot.send_message(message.message.chat.id,teams + "\nИгра началась!")

def stopGame(now_chat, message, from_who):
    isGameStop = now_chat.gameStop(from_who)
    if(isGameStop == 0):
        bot.answer_callback_query(message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif (isGameStop == 1):
        bot.answer_callback_query(message.id, 'Игра даже не началась, отменять нечего.')
        return
    elif (isGameStop == 2):
        bot.answer_callback_query(message.id, 'Отменять нечего.')
    elif (isGameStop == 3):
        bot.send_message(message.message.chat.id, '%s отменил игру.' % from_who)

def winGame(now_chat, message, from_who):
    isResult = now_chat.writeResult(True, from_who)
    if(isResult == 0):
        bot.answer_callback_query(message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif(isResult == 1):
        bot.answer_callback_query(message.id, 'Игра даже не началась.')
        return
    else:
        bot.send_message(message.message.chat.id, '%s объявил победу своей команды.' % from_who)

def loseGame(now_chat, message, from_who):
    isResult = now_chat.writeResult(False, from_who)
    if(isResult == 0):
        bot.answer_callback_query(message.id, 'Ты не создатель игры, иди лесом.')
        return
    elif(isResult == 1):
        bot.answer_callback_query(message.id, 'Игра даже не началась.')
        return
    else:
        bot.send_message(message.message.chat.id, '%s объявил поражение своей команды.' % from_who)


@bot.message_handler(commands=['start'])
def start(message):
    # global isStartPressed
    # if(isStartPressed is True):
    #     bot.send_message(message.chat.id, "Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.", reply_markup=gen_markup())
    #     #bot.send_message(message.chat.id, 'Бот уже работает, тебе заняться нечем?')
    #     return
    
    # isStartPressed = True

    now_chat = chat.Chat(conn)
    global chats
    chats[message.chat.id] = now_chat
    #bot.send_message(message.chat.id, 'Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.')    

    # e1 = threading.Event()
    # t1 = threading.Thread(target=test_timer, args=(message,1800))
    # t1.start()
    # e1.set()

    bot.send_message(message.chat.id, "Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.", reply_markup=gen_markup())

@bot.message_handler(commands=['help'])
def help(message):
    # global isStartPressed
    # if(isStartPressed is False):
    #     bot.send_message(message.chat.id, 'Напишите /start')
    #     return

    bot.send_message(message.chat.id, 'Вот, что я могу:\n', reply_markup=gen_markup())

@bot.message_handler(regexp="\w*\s*ф\w*\s*у\w*\s*т\w*\s*б\w*\s*о\w*\s*л")
def footballMsg(message):
     chat_id =  message.chat.id
     bot.send_message(message.chat.id, "Ага, я что-то услышал про футбол...\n", reply_markup=gen_markup())

@bot.message_handler(regexp="\w*\s*f\w*\s*o\w*\s*o\w*\s*t\w*\s*b\w*\s*a\w*\s*l\w*\s*l")
def footballMsg(message):
     bot.send_message(message.chat.id, "Ага, я что-то услышал про футбол...\n", reply_markup=gen_markup())

# @bot.message_handler(content_types=["sticker"])
# def handle_sticker(message):
#      bot.send_sticker(message.chat.id, 'CAACAgIAAx0CaHeRXAACGkVjDHTIvjP2EMLWCFJ3I6gfDV8V_gAC0RYAAjqeIEkTD5Q3eXcgCikE')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    # global isStartPressed
    # if(isStartPressed is False):
    #     bot.send_message(call.message.chat.id, 'Напишите /start')
    #     return
    message = call.message
    global chats
    key = call.message.chat.id
    if(key not in chats):
        now_chat = chat.Chat(conn)
        chats[key] = now_chat
    else: 
        now_chat = chats[key]

    my_scope = now_chat.getMe(call.from_user.first_name)
    if(my_scope == -1):
        bot.answer_callback_query(call.id, call.from_user.first_name + ', зарегайся сначала, чукча.\nКоманда /reg' )
        return

    if call.data == "mystat": 
        bot.send_message(call.message.chat.id, call.from_user.first_name + ', твой ранг - %s. Давай поднажми, осталось совсем немного до нового ранга.' % my_scope)
        #bot.send_message(message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())
    elif call.data == "allstat":
        bot.send_message(call.message.chat.id, now_chat.getAll())
        #bot.send_message(message.chat.id, "\nЧто ещё могу предложить:", reply_markup=gen_markup())
    elif call.data == "create_game":
        createGameFunction(now_chat, call, call.from_user.first_name)
    elif call.data == "top_joke":
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
        getAnektod(call, now_chat)

    bot.answer_callback_query(call.id, "")

@bot.message_handler(regexp="\/\w+[@\w]*")
def handle_text(message):
    # global isStartPressed
    # if(isStartPressed is False):
    #     bot.send_message(message.chat.id, 'Напишите /start')
    #     return

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

    isReg = now_chat.registration(message.from_user.first_name, message.from_user.id)

    if (text == "/reg" or text == "/reg@qakickerratingbot"):
        if(isReg is True):
            bot.send_message(chat_id, message.from_user.first_name + ', ты зарегался и сейчас у тебя TRAINEE I ранг.\nДумал все так просто будет?')
        else:
            bot.send_message(chat_id, message.from_user.first_name + ', ты уже зарегался')

bot.polling(none_stop=True, interval=0)
