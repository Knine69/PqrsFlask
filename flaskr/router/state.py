from flask import Blueprint, request, jsonify
from ..router.sqlstatements import get_one_from_table, create_statements_block, get_all_entities, delete_from_table, create_new_state
from ..router.utils.utils import return_table_name, PATCH_STORED_PROCEDURE, fetch_resources
from ..domain.config import Config
import json

router_state = Blueprint('router_state', __name__, template_folder='templates', url_prefix='/state')
mysql = Config.give_mysql_instance()

table_name = return_table_name(router_state)

@router_state.route('/<int:id>', methods=["GET"])
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(get_one_from_table().format(table_name, table_name), create_statements_block({"id": id}))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

@router_state.get('/')
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(get_all_entities().format(table_name))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

@router_state.post("/new_state")
def insert_new_state():
    """
    Creates new state based on a received body sent from the Web Server
    """
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        cur = mysql.connection.cursor()
        cur.execute(create_new_state(), create_statements_block(request_data))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

    return "Insert successfull"

@router_state.delete("/<int:id>")
def delete_state(id):
    """
    Deletes a specific state based on a given ID

    id: Given ID to delete in database
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(delete_from_table().format(table_name, table_name), (id,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

    return "Delete successfull"

@router_state.patch("/<int:id>")
def update_state(id):
    """
    Updates a state in database based on the received elements from a JSON coming from the Web Server
    """
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
