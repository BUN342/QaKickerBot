class Result:

    def writeResult(self, players, cursor):
        sql = "INSERT INTO users (tg_name, scope) VALUES (%s, %s);"
        data = (userName, 0)
        cursor.execute(sql, data)