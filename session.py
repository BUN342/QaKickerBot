class Session:

    def createSession(self, newScope, userName, cursor):
        sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
        data = (userName, 0)
        cursor.execute(sql, data)

    def writeUser(self, userName, cursor):
        sql = """SELECT * FROM users WHERE tg_name = %s;"""
        data = (userName,)
        cursor.execute(sql, data)
        results = cursor.fetchall()
        if not results:
            return True
        else:
            return False

    def sessionCheck(self, newScope, userName, cursor):
        sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
        data = (userName, 0)
        cursor.execute(sql, data)

    def userCheck(self, newScope, userName, cursor):
        sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
        data = (userName, 0)
        cursor.execute(sql, data)