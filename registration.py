class Registration:
    # def __init__(self, name, scope):
    #     self.__tg_name=name
    #     self.__scope=scope

    def register(self, userName, userId, cursor):
        sql = "INSERT INTO users (tg_name, tg_id, scope) VALUES (%s, %s);"
        data = (userName, userId, 0)
        cursor.execute(sql, data)

    def regCheck(self, userName, userId, cursor):
        sql = """SELECT * FROM users WHERE tg_id = %s;"""
        data = (userId,)
        cursor.execute(sql, data)
        results = cursor.fetchall()
        if not results:
            return True
        else:
            return False