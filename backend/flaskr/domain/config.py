from flask_mysqldb import MySQL
_mysql = MySQL()

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'pqrs'
    MYSQL_CURSORCLASS = 'DictCursor'

    def give_mysql_instance():
        return _mysql