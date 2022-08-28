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
        self.__player[userName] = self.__side
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
        self.__isGameNow = True
    def gameStop(self,): 
        self.__isGameNow = False
        self.__players = {}
    def getMe(self, userName):
         usr = user.User()
         return usr.getScope(userName, self.__cursor)