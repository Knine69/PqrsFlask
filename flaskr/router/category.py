from flask import Blueprint, request, jsonify
from ..router.sqlstatements import get_one_from_table, create_statements_block, get_all_entities, delete_from_table, create_new_category
from ..router.utils.utils import return_table_name, fetch_resources, PATCH_STORED_PROCEDURE, ERROR_MESSAGE, ALLOWED_ORIGINS
from ..domain.config import Config
import json

router_category = Blueprint('router_category', __name__, template_folder='templates', url_prefix='/category')
mysql = Config.give_mysql_instance(self=Config)

table_name = return_table_name(router_category)

@router_category.route('/<int:id>', methods=["GET"])
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
        error_message = ERROR_MESSAGE.format(str(e))
        return jsonify(error_message), 500

@router_category.get('/')
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    try:
        origin = request.headers["origin"]
        if  origin in ALLOWED_ORIGINS:
            cur = mysql.connection.cursor()
            cur.execute(get_all_entities().format(table_name))
            data = cur.fetchall()
            cur.close()

            response = jsonify(data)
            response.headers["Access-Control-Allow-Origin"] = origin
            return response
    except Exception as e:
        error_message = ERROR_MESSAGE.format(str(e))
        return jsonify(error_message), 500

@router_category.post("/new_category")
def insert_new_category():
    """
    Creates new category based on a received body sent from the Web Server
    """
    try:
        request_data = json.loads(request.data.decode('utf-8'))
        cur = mysql.connection.cursor()
        cur.execute(create_new_category(), create_statements_block(request_data))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        error_message = ERROR_MESSAGE.format(str(e))
        return jsonify(error_message), 500

    return "Insert successfull"

@router_category.delete("/<int:id>")
def delete_category(id):
    """
    Deletes a specific category based on a given ID

    id: Given ID to delete in database
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(delete_from_table().format(table_name, table_name), (id,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        error_message = ERROR_MESSAGE.format(str(e))
        return jsonify(error_message), 500

    return "Delete successfull"


@router_category.patch("/<int:id>")
def update_category(id):
    """
    Updates a category in database based on the received elements from a JSON coming from the Web Server
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
        error_message = ERROR_MESSAGE.format(str(e))
        return jsonify(error_message), 500
