from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from sqlstatements import *
from utils import *
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('pqrs_corpus.html', logged=True, message="This is my landing page at home!")

@app.route('/data/<string:table_name>/<int:id>', methods=["GET"])
def get_single_entry(table_name, id):
    """
    Brings a specific registry from a specific table dynamically.

    table_name: Gives the specific table name
    id: Gives the specific ID to look for in the database
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(get_one_from_table(), create_statements_block({"table": table_name, "table_name": table_name, "id": id}))
        data = cur.fetchall()
        cur.close()
        return render_template('pqrs_corpus.html', data = passdown_response(True, True, data, table_name))
    except:
        return render_template('pqrs_corpus.html', logged=True,  data = passdown_empty())

@app.get('/data/<string:table_name>')
def get_all(table_name):
    """
    Brings a all entries from a specific table dynamically.

    table_name: Gives the specific table name
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(get_all(), create_statements_block({"table": table_name}))
        data = cur.fetchall()
        cur.close()
        return render_template('pqrs_corpus.html', data = passdown_response(True, True, data, table_name))
    except:
        return render_template('pqrs_corpus.html', logged=True,  data = passdown_empty())

@app.post("/new_person")
def insert_new_person():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        cur = mysql.connection.cursor()
        cur.execute(create_new_person(), create_statements_block(request_data))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return e

    return "Insert successfull"

@app.post("/new_role")
def insert_new_role():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        cur = mysql.connection.cursor()
        cur.execute(create_new_role(), create_statements_block(request_data))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        return e

    return "Insert successfull"

