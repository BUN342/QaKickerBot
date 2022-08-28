class Registration:
    # def __init__(self, name, scope):
    #     self.__tg_name=name
    #     self.__scope=scope

    def register(self, userName, cursor):
        sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
        data = (userName, 0)
        cursor.execute(sql, data)

    def regCheck(self, userName, cursor):
        sql = """SELECT * FROM users WHERE tg_name = %s;"""
        data = (userName,)
        cursor.execute(sql, data)
        results = cursor.fetchall()
        if not results:
            return True
        else:
            return False