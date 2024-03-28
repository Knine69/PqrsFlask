from flask import Blueprint, request, jsonify
from ..router.sqlstatements import *
from ..router.utils.utils import *
from ..domain.config import Config
import json

router_category = Blueprint('router_category', __name__, template_folder='templates', url_prefix='/category')
mysql = Config.give_mysql_instance()

table_name = return_table_name(router_category)

@router_category.route('/<int:id>', methods=["GET"])
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
        return json.dumps(data)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

@router_category.get('/')
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
        return json.dumps(data)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

@router_category.post("/new_category")
def insert_new_category():
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        cur = mysql.connection.cursor()
        cur.execute(create_new_category(), create_statements_block(request_data))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

    return "Insert successfull"

@router_category.delete("/<int:id>")
def delete_category(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(delete_from_table().format(table_name, table_name), (id,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

    return "Delete successfull"


@router_category.patch("/<int:id>")
def update_category(id):
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        cur = mysql.connection.cursor()
        cur.callproc(PATCH_STORED_PROCEDURE, [table_name, id, json.dumps(request_data)])
        response = fetch_resources(cur)
        mysql.connection.commit()
        cur.close()

        return jsonify(response[0])
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500
