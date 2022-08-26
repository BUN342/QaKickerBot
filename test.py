from cmath import nan
import psycopg2
from collections import defaultdict
import telebot
from datetime import datetime, timedelta
from telebot import types

TOKEN="5732654013:AAEs3Ke5uPUMiZBUk03DitDVVmteGiVENEE"
bot = telebot.TeleBot(TOKEN)
 
user = 'mdriysdmzxohga'
password = 'd5016c9242569d17b84950f4d0cb9ba3be135fbdff7d89e09f96785d5845e9a2'
db_name = 'dbf5g5orv48dsr'
host='ec2-34-242-8-97.eu-west-1.compute.amazonaws.com'
port = 5432
rank = "TRAINEE I"
POOL_TIME_FOR_GAME=5

conn = psycopg2.connect(dbname=db_name, user=user, 
                        password=password, host=host)

class User:
    def __init__(self, name, scope):
        self.__tg_name=name
        self.__scope=scope

    def setName(self) : return
    def setScope(self, newScope):
        self.__scope=newScope

    def getName(self):
        return self.__tg_name
    def getScope(self):
        return self.__scope
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я - бот для подсчета вашего рейтинга.\nНапишите /help, чтобы узнать больше.')

@bot.message_handler(commands=['help'])
def help(message):
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
    text = message.text.lower()
    chat_id =  message.chat.id

    cursor = conn.cursor()
    sql = """SELECT * FROM users WHERE tg_name = %s;"""
    data = (message.from_user.first_name,)
    cursor.execute(sql, data)
    results = cursor.fetchall()

    # #user = User(message.from_user.first_name, 0)
    # if(message.from_user.first_name == "Yuriy"):
    #      bot.send_message(message.chat.id, "Юра, нет")
    # if message.chat.type == "private":
    #     return
    if (text != "/reg" and text != "/reg@qakickerratingbot") and not results:
        bot.send_message(chat_id, "Ты даже не зарегался\nНапиши /reg, рак")
    elif text == "/reg" or text == "/reg@qakickerratingbot":
        if not results:
            
            sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
            data = (message.from_user.first_name, 0)

            cursor.execute(sql, data)
            conn.commit()
            
            
            bot.send_message(chat_id, message.from_user.first_name + ', ты зарегался и сейчас у тебя TRAINEE I ранг.\nДумал все так просто будет?')
        else:
            bot.send_message(chat_id, message.from_user.first_name + ', ты уже зарегался')
    elif text == "/game4" or text == "/game4@qakickerratingbot":
        date = datetime.utcnow()-timedelta(minutes=POOL_TIME_FOR_GAME)
        
        sql = "SELECT last_upd FROM game_sessions WHERE last_upd > TIMESTAMP%s ORDER BY last_upd DESC;"
        #data = (round(date.timestamp()),)
        data = (date,)
        cursor.execute(sql, data)
        is_games = cursor.fetchone()

        if(is_games is not None):
            bot.send_message(chat_id, 'Игру уже кто-то начал.\nЗаверши предыдущую, прежде чем начать новую.')
            return

        bot.send_message(chat_id, 'Так, так, так.. Кто это тут у нас хочет начать игру?\nДавайте поможем %s собрать участников, пиши /me, если хочешь присоединиться к игре.' % message.from_user.first_name)
        
        
        sqlINS = "INSERT INTO game_sessions (tg_name, win, chat_id, last_upd, game_id, side) VALUES (%s, %s, %s, %s, %s, %s);"
        
        data = (message.from_user.first_name, None, chat_id, datetime.utcnow(), message.from_user.id, True)
        cursor.execute(sqlINS, data)
        
        conn.commit()
    elif text == "/me" or text == "/me@qakickerratingbot":
        side = True
        date = datetime.utcnow()-timedelta(minutes=POOL_TIME_FOR_GAME)

        

        sql = "SELECT tg_name FROM game_sessions WHERE tg_name = %s AND last_upd > TIMESTAMP%s ORDER BY last_upd DESC;"
        data = (message.from_user.first_name,date)

        cursor.execute(sql, data)
        is_player = cursor.fetchall()
        

        if is_player is not None:
            bot.send_message(chat_id, '%s, ты уже записался на игру, жди начала' % message.from_user.first_name)
            return
        

        
        sql="SELECT game_id, last_upd, side FROM game_sessions WHERE chat_id = %s AND last_upd > TO_TIMESTAMP(%s) ORDER BY last_upd DESC;"
        data=(chat_id, round(date.timestamp()))

        cursor.execute(sql, data)
        last_game = cursor.fetchall()
        

        if last_game is None:
            bot.send_message(chat_id, 'Данных нет!')
        elif(round(date.timestamp()) >= last_game[0][1].timestamp()):
            bot.send_message(chat_id, 'Игр нет!')
        else:        
            sql="INSERT INTO game_sessions (tg_name, win, chat_id, last_upd, game_id, side) VALUES (%s, %s, %s, %s, %s, %s);"        
            
            if side is True:
                data = (message.from_user.first_name, None, chat_id, datetime.utcnow(), last_game[0][0], True)
                cursor.execute(sql, data)
                side = False
            else:
                data = (message.from_user.first_name, None, chat_id, datetime.utcnow(), last_game[0][0], False)
                cursor.execute(sql, data)
                side = True

            bot.send_message(chat_id, 'Все готовы?\nПишите /gamestart, чтобы начать игру.\nИли /gamestop, если хотите отменить игру')

            conn.commit()
            
    elif text == "/gamestart" or text == "/gamestart@qakickerratingbot":
            bot.send_message(chat_id, 'Игра началась!\n*дальнейший функционал будет готов в следующем релизе*')
    elif text == "/gamestop" or text == "/gamestop@qakickerratingbot":
            bot.send_message(chat_id, 'Чё, обоссались?\n*дальнейший функционал будет готов в следующем релизе*')
    elif text == "/mystat" or text == "/mystat@qakickerratingbot": 
        
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (message.from_user.first_name,)
        cursor.execute(sqlSEL, data)
        my_scope = cursor.fetchall()

        sql = "SELECT name, max_scope FROM grades ORDER BY max_scope ASC"
        cursor.execute(sql)
        grades = cursor.fetchall()
        

        j = 0
        for i in grades:
            if i[1] > my_scope[0][0]:
                if(j == 0):
                    j += 1
                
                global rank
                rank = i[0]
                break
            else:
                j += 1
                
        bot.send_message(chat_id, message.from_user.first_name + ', твой ранг - %s. Давай поднажми, осталось совсем немного до нового ранга.' % rank)
            
    elif text == "/allstats" or text == "/allstats@qakickerratingbot":
        
        sqlSEL = "SELECT tg_name, scope FROM users ORDER BY scope DESC;"
        cursor.execute(sqlSEL)
        scopes_with_names = cursor.fetchall()

        sql = "SELECT name, max_scope FROM grades ORDER BY max_scope ASC"
        cursor.execute(sql)
        grades = cursor.fetchall()
        

        stat = "Рейтинг среди футболёров: \n"
        for n in scopes_with_names:
            for i in grades:        
                if i[1] > n[1]:
                    stat += '\t\t\t' + str(n[0]) + ', ранг - %s, очков - %s.' % (str(i[0]), n[1]) + '\n'
                    break       
        bot.send_message(chat_id, stat)

# Запускаем бота
bot.polling(none_stop=True, interval=0)