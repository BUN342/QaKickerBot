import user
import registration
import joke

class Chat:
    def __init__(self, connection):
        #self.__chatId=chatId
        self.__isGameNow=False
        self.__regBegin=False
        self.__connection=connection
        self.__cursor=connection.cursor()
        self.__players={}
        self.__side = True
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
        self.__side = True
        if(self.__isGameNow is True):
            return False
        elif(len(self.__players) != 0):
            return False

        self.__regBegin = True
        self.__creatorOfGame = userName
        self.__players[userName] = self.__side
        return True

    def writeUserToGame(self,userName):
        if(self.__isGameNow is True and len(self.__players) >= 4):
            return 1
        elif(len(self.__players) >= 4):
            return 2      
        elif(userName in self.__players):
            return 3
        elif(self.__regBegin is False):
            return 4

        

        if(self.__side is True):
            self.__side = False
        else:
            self.__side = True
        self.__players[userName] = self.__side

        return self.__players
    def writeResult(self, result, userName): 
        if((self.__isGameNow is True or self.__regBegin is True) and userName != self.__creatorOfGame):
            return 0
        elif(self.__isGameNow is False):
            return 1
        
        if(result is True):
            winSide = self.__players[userName]
        else:
            if(self.__players[userName] is True):
                winSide = False
            else:
                winSide = True

        usr = user.User()

        for player in self.__players:
            if(self.__players[player] == winSide):
                usr.setScope(True, player, self.__cursor)
            else:
                usr.setScope(False, player, self.__cursor)
            self.__connection.commit()
   

        self.__regBegin = False
        self.__isGameNow = False
        return self.__players
    
    def gameStart(self,userName): 
        if(self.__regBegin is True and userName != self.__creatorOfGame):
            return 0
        elif(len(self.__players) < 2 or len(self.__players) == 3):
            return 1
        elif(self.__isGameNow is True):
            return 2

        self.__isGameNow = True
        self.__regBegin = False 
        return self.__players

    def gameStop(self,userName): 
        if(userName != self.__creatorOfGame):
            return 0
        elif(len(self.__players) > 0):
            self.__players = {}
            self.__isGameNow = False
            self.__regBegin = False
            return 3
        elif (len(self.__players) == 0):
            return 2
        elif(self.__isGameNow is False): 
            self.__players = {}
            return 1
#1
        self.__isGameNow = False
        self.__players = {}
        self.__regBegin = False

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
    
    def getHohma(self, type_hohma):

        hohma = joke.Joke()
        answer = ""

        if(type_hohma == '1'):
            answer = hohma.getJoke()
        else:
             answer = hohma.getAnekdot(self.__cursor)
             self.__connection.commit()
        
        return answer