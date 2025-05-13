import pymysql
import pymysql.cursors

class Database:
    def __init__(self, host, port, database, user, password) -> None:
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def query(self, sql:str, *args) -> list | None:
        connection = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        cursor = connection.cursor(pymysql.cursors.DictCursor)

        sql = sql.strip()

        if not args:
            args = None

        cursor.execute(sql, args)
        result = cursor.fetchall()

        connection.commit()

        cursor.close()
        connection.close()

        return result