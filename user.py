class User:
    # def __init__(self, name, scope):
    #     self.__tg_name=name
    #     self.__scope=scope

    def setScope(self, result, side, userName, cursor):
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (userName,)
        cursor.execute(sqlSEL, data)
        user_scope = cursor.fetchall()
        coins = user_scope[0][0]
        
        if(coins==0):
            return False
            bot.send_message(message.chat.id, 'Не от чего отнимать рейтинг')
        elif(coins < 25 and coins >= 0):
            coins = 0
        else:
            if(result is True):
                coins +=25
            else:
                coins -=25
        
        sqlUPD = "UPDATE users SET scope = %s WHERE tg_name = %s;"
        data = (coins, userName)
        cursor.execute(sqlUPD, data)
        return True

    def getName(self):
        return self.__tg_name

    def getScope(self, userName, cursor):
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (userName,)
        cursor.execute(sqlSEL, data)
        my_scope = cursor.fetchall()
        return my_scope