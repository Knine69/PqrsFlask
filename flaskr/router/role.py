from flask import Blueprint, render_template, request
from router.sqlstatements import *
from router.utils import *
from domain.config import Config
import json

router_role = Blueprint('router_role', __name__, template_folder='templates', url_prefix='/role')
mysql = Config.give_mysql_instance()
table_name = return_table_name(router_role)

@router_role.route('/<int:id>', methods=["GET"])
def get_single_entry(id):
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

@router_role.get('/')
def get_all():
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

@router_role.post("/new_role")
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