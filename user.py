class User:
    # def __init__(self, name, scope):
    #     self.__tg_name=name
    #     self.__scope=scope

    def setScope(self, result, userName, cursor):
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (userName,)
        cursor.execute(sqlSEL, data)
        user_scope = cursor.fetchall()
        coins = user_scope[0][0]            
        
        if(coins < 25 and coins >= 0):
            coins = 0
        else:
            if(result is True):
                coins +=25
            else:
                if(coins==0):
                    coins = 0
                else:
                    coins -=25
        
        sqlUPD = "UPDATE users SET scope = %s WHERE tg_name = %s;"
        data = (coins, userName)
        cursor.execute(sqlUPD, data)

    def getName(self):
        return self.__tg_name

    def getScope(self, userName, cursor):
        sqlSEL = "SELECT scope FROM users WHERE tg_name = %s;"
        data = (userName,)
        cursor.execute(sqlSEL, data)
        my_scope = cursor.fetchall()

        sql = "SELECT name, max_scope FROM grades ORDER BY max_scope ASC"
        cursor.execute(sql)
        grades = cursor.fetchall()

        global rank
        j = 0
        for i in grades:
            if i[1] > my_scope[0][0]:
                if(j == 0):
                    j += 1
                
                rank = i[0]
                break
            else:
                j += 1

        return rank