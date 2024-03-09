from flask import Blueprint, render_template, request
from router.sqlstatements import *
from router.utils import *
from flask_mysqldb import MySQL
import json

router = Blueprint('router', __name__, template_folder='templates')
mysql = MySQL()

@router.route("/")
def home():
    return render_template('pqrs_corpus.html', logged=True, message="This is my landing page at home!")

@router.route('/data/<string:table_name>/<int:id>', methods=["GET"])
def get_single_entry(table_name, id):
    """
    Brings a specific registry from a specific table dynamically.

    table_name: Gives the specific table name
    id: Gives the specific ID to look for in the database
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(get_one_from_table().format(table_name, table_name), create_statements_block({"id": id}))
        data = cur.fetchall()
        cur.close()
        return render_template('pqrs_corpus.html', data = passdown_response(True, True, data, table_name))
    except Exception as e:
        return e

@router.get('/data/<string:table_name>')
def get_all(table_name):
    """
    Brings a all entries from a specific table dynamically.

    table_name: Gives the specific table name
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(get_all_entities().format(table_name))
        data = cur.fetchall()
        cur.close()
        return render_template('pqrs_corpus.html', data = passdown_response(True, True, data, table_name))
    except Exception as e:
        return e

@router.post("/new_person")
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

@router.post("/new_role")
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

