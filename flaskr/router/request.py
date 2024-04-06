from flask import Blueprint, request, jsonify
from ..router.sqlstatements import get_request_information, create_statements_block, get_all_entities, delete_from_table, create_new_request
from ..router.utils.utils import return_table_name, PATCH_STORED_PROCEDURE, fetch_resources, give_new_request_body, get_category_id_by_name, get_person_by_document_id
from ..domain.config import Config
import json

router_request = Blueprint('router_request', __name__, template_folder='templates', url_prefix='/request')
mysql = Config.give_mysql_instance()

table_name = return_table_name(router_request)

@router_request.route('/<int:id>', methods=["GET"])
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    try:
        cur = mysql.connection.cursor()
        cur.execute(get_request_information(), create_statements_block({"id": id}))
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

@router_request.get('/')
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


@router_request.post("/new_request")
def insert_new_request():
    """
    Creates new request based on a received body sent from the Web Server
    """
    try:
        request_data = _adapt_request_data_new_request()
        if not request_data["error"]:
            cur = mysql.connection.cursor()
            cur.execute(create_new_request(), create_statements_block(give_new_request_body(request_data)))
            mysql.connection.commit()
            cur.close()
            return {       
                "Description": "Insert successfull"
                }
        return jsonify({"error": request_data["error"]}), 404
    except Exception as e:
        error_message = "An error occurred: {}".format(str(e))
        return jsonify(error_message), 500

    

@router_request.delete("/<int:id>")
def delete_request(id):
    """
    Deletes a specific request based on a given ID

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

@router_request.patch("/<int:id>")
def update_request(id):
    """
    Updates a request in database based on the received elements from a JSON coming from the Web Server
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

def _get_category(data):
    return get_category_id_by_name(mysql, data)

def _get_person(data):
    return get_person_by_document_id(mysql, data)

def _adapt_request_data_new_request():
    request_data = json.loads(request.data.decode('utf-8'))
    request_data.update(_get_category(request_data["category"]))
    request_data.update(_get_person(request_data["documentId"]))

    request_data.pop("category")
    request_data.pop("documentId")

    return request_data