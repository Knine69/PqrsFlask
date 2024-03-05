from flask import Flask, render_template, jsonify
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'pqrs'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('pqrs_corpus.html', logged=_is_logged(), message="This is my landing page at home!")

@app.route('/data/<string:table_name>/<int:id>', methods=["GET"])
def get_single_entry(table_name, id):
    """
    Brings a specific registry from a specific table dynamically.

    table_name: Gives the specific table name
    id: Gives the specific ID to look for in the database
    """
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM {table} WHERE {table}_id = %s'''.format(table = table_name), (id,))
    data = cur.fetchall()
    cur.close()
    passdown = {
        "logged" : True,
        "table_information" : True,
        "response_table" : data,
        "table_name" : table_name
    }
    return render_template('pqrs_corpus.html', data = passdown)

    return jsonify(data).get_json

@app.get('/data/<string:table_name>')
def get_all(table_name):
    """
    Brings a all entries from a specific table dynamically.

    table_name: Gives the specific table name
    """

    try:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM {table}'''.format(table = table_name))
        data = cur.fetchall()
        cur.close()
        passdown = {
            "logged" : True,
            "table_information" : True,
            "response_table" : data,
            "table_name" : table_name
        }
        return render_template('pqrs_corpus.html', data = passdown)
    except:
        return render_template('pqrs_corpus.html', logged=True, tableinformation = False, response_table = None)


def _is_logged():
    return True
