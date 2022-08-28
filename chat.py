import user
import registration

class Chat:
    def __init__(self, connection):
        #self.__chatId=chatId
        self.__isGameNow=False
        self.__connection=connection
        self.__cursor=connection.cursor()
        self.__players={}
        self.__side = 0
        self.__creatorOfGame = ""
    
    
    def registration(self, userName): 
        reg = registration.Registration()
        if reg.regCheck(userName, self.__cursor) is True:
            reg.register(userName, self.__cursor)
            self.__connection.commit()
            return True
        else:
            return False

    def createGame(self,userName):
        if(self.__isGameNow is True):
            return False
        elif(len(self.__players) != 0):
            return False

        self.__creatorOfGame = userName
        self.__players[userName] = self.__side
        self.__side = 1
        return True

    def writeUserToGame(self,userName):
        if(self.__isGameNow is True):
            return False
        elif(len(self.__players) == 0 or len(self.__players) >= 4):
            return False      
        elif(userName in self.__players):
            return False

        self.__player[userName] = self.__side

        if(self.__side == 1):
            self.__side = 0
        else:
            self.__side = 1

        return True
    def writeResult(self, result, userName): 
        if(self.__isGameNow is True):
            return False

        if(userName != self.__creatorOfGame):
            return False

        usr = user.User()
        for player in self.__players:         
            usr.setScope(result, player[1], player[0], self.__cursor)
            self.__connection.commit()
    
    def gameStart(self,): 
        if(len(self.__players) < 2):
            return False
        self.__isGameNow = True
    def gameStop(self,): 
        self.__isGameNow = False
        self.__players = {}
    def getMe(self, userName):
         usr = user.User()
         return usr.getScope(userName, self.__cursor)
    def getAll(self,):
        usr = user.User()
        sqlSEL = "SELECT tg_name, scope FROM users ORDER BY scope DESC;"
        self.__cursor.execute(sqlSEL)
        scopes_with_names = self.__cursor.fetchall()

        sql = "SELECT name, max_scope FROM grades ORDER BY max_scope ASC"
        self.__cursor.execute(sql)
        grades = self.__cursor.fetchall()

        stat = "Рейтинг среди футболёров: \n"
        for n in scopes_with_names:
            for i in grades:        
                if i[1] > n[1]:
                    stat += '\t\t\t' + str(n[0]) + ', ранг - %s, очков - %s.' % (str(i[0]), n[1]) + '\n'
                    break       
        return stat