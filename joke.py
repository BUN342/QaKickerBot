import random
import pyjokes

class Joke:

  def getJoke(self,):
    joke = pyjokes.get_joke()
    return joke
  
  def getAnekdot(self, cursor):
    # sqlSEL = "SELECT MAX(id) FROM anek;"
    # cursor.execute(sqlSEL)
    # maxID = cursor.fetchone()

    # randomValue = random.randint(1,maxID[0])
 
    sqlSEL = "SELECT id, text FROM anek WHERE status IS FALSE ORDER BY random() LIMIT 1;"

    cursor.execute(sqlSEL)
    result = cursor.fetchone()

    sqlUPD = "UPDATE anek SET status = true WHERE id = %s;"
    data = (result[0],)
    cursor.execute(sqlUPD, data)

    return result[1].replace('\\n','\n')