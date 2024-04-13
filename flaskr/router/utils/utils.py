from flask import Blueprint, jsonify
from datetime import datetime

PATCH_STORED_PROCEDURE = 'PatchRecordsInTable'
GET_CATEGORY_NAME_PROCEDURE = 'GetCategoryByName'
GET_PERSON_BY_DOCUMENT_PROCEDURE = 'GetPersonByDocumentId'
ERROR_MESSAGE="An error occurred: {}"
_STATE_ID_NEW_REQUEST = 1
ALLOWED_ORIGINS= ["http://localhost:3000"]

def fetch_resources(cur):
    main_result = cur.fetchall()
    remaining_result_sets = []
    while cur.nextset():
        remaining_result_sets.append(cur.fetchall())

    return [main_result, remaining_result_sets]

def get_category_id_by_name(mysql, category_name):
    try:
        cur = mysql.connection.cursor()
        cur.callproc(GET_CATEGORY_NAME_PROCEDURE, [category_name])
        response = fetch_resources(cur)
        return {"category_id": response[0][0]['category_id']}
    except Exception as e:
        error_message = ERROR_MESSAGE.format(str(e))
        return jsonify(error_message), 500


def get_person_by_document_id(mysql, document_id):
    try:
        cur = mysql.connection.cursor()
        cur.callproc(GET_PERSON_BY_DOCUMENT_PROCEDURE, [document_id])
        response = fetch_resources(cur)
        return {"requester_id": response[0][0]['person_id'], "error": None}
    except Exception:
        return {
            "error": "Person does not exist"
        }

def give_new_request_body (request_data):
    return {
        "generated_at": datetime.now().strftime('%Y-%m-%d'),
        "summary": request_data["summary"],
        "category_id": request_data["category_id"],
        "requester_id": request_data["requester_id"],
        "state_id": _STATE_ID_NEW_REQUEST
    }

def return_table_name(router: Blueprint):
    return router.url_prefix[1:]