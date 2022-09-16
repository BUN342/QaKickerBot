import user
import registration
import joke
import praw
from requests import Session
from random import randint

#bot_memes123
#buruni123

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
        self.__isAnek = False
    
    
    def registration(self, userName, userId): 
        reg = registration.Registration()
        if reg.regCheck(userId, self.__cursor) is True:
            reg.register(userName, userId, self.__cursor)
            self.__connection.commit()
            return True
        else:
            return False

    def createGame(self,userName):
        self.__regBegin=True
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
        self.__isGameNow = False

        for player in self.__players:
            if(self.__players[player] == winSide):
                usr.setScope(True, player, self.__cursor)
            else:
                usr.setScope(False, player, self.__cursor)
            self.__connection.commit()
   
        self.gameStop(self.__creatorOfGame)
        return self.__players
    
    def gameStart(self,userName): 
        if(self.__regBegin is True and userName != self.__creatorOfGame):
            return 0
        elif(len(self.__players) <= 3):
            return 1
        elif(self.__isGameNow is True):
            return 2
        elif(userName != self.__creatorOfGame):
            return 3

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

    def getMe(self, userId):

         usr = user.User()

         return usr.getScope(userId, self.__cursor)

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
        # if(self.__isAnek is True and type_hohma != 1):
        #     return -1
        # else:
        #     self.__isAnek = True
        hohma = joke.Joke()
        answer = ""

        if(type_hohma == 1):
            answer = hohma.getJoke()
        else:
             answer = hohma.getAnekdot(self.__cursor)
             self.__connection.commit()
        
        return answer


    def getMem(self,):
        # r = requests.get('https://www.reddit.com/r/dankmemes/search.json?q=mem')
        # random_number = randint(1, 100)
        # print(len(r.text.data.children))

        reddit = praw.Reddit(
            client_id="Inrbm3kN-i-eNNOmdX7aJA",
            client_secret="	2MJ_iAus_p5WJpgSEiD5XfPDp0_2FQ",
            user_agent="python"
        )
        for submission in reddit.subreddit("learnpython").hot(limit=10):
            print(submission.title)


        # sub = "dankmemes"
        # count = 4
        # sub_reddit = reddit.subreddit(sub)
        # hot_meme = sub_reddit.hot(limit=count)
        # result =[]
        # for submissions in hot_meme:
        #     print(submissions.title)