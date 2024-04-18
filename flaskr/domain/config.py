from flask_mysqldb import MySQL

class Config:
    _mysql = MySQL()
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'pqrs'
    MYSQL_CURSORCLASS = 'DictCursor'

    def give_mysql_instance(self):
        return self._mysql