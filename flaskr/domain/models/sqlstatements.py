from ...application.router.utils.utils import get_category_id_by_name

def get_one_from_table():
    return """SELECT * FROM {} where {}_id = %s"""

def get_all_entities():
    return """SELECT * FROM {}"""

def get_person_information():
    return """SELECT s.* FROM (select @person_id:= %s p) parm , LookUpPersonInformation s;"""

def get_request_information():
    return """SELECT s.* FROM (select @request_id:= %s p) parm , LookUpRequestInfo s;"""

def get_person_requests():
    return """SELECT s.* FROM (select @person_id:=%s p) parm , LookUpPersonRequests s;"""

def create_new_role():
    return """INSERT INTO role (name) VALUES (%s)"""

def create_new_state():
    return """INSERT INTO state (name) VALUES (%s)"""

def create_new_position():
    return """INSERT INTO position (name) VALUES (%s)"""

def create_new_category():
    return """INSERT INTO category (name) VALUES (%s)"""

def create_new_department():
    return """INSERT INTO department (name, active_members) VALUES (%s, %s)"""

def create_new_person():
    return """INSERT INTO person (name, document_id, email, position_id, role_id, department_id, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

def create_new_request():
    return """INSERT INTO request (generated_at, summary, category_id, requester_id, state_id) VALUES (%s, %s, %s, %s, %s)"""

def delete_from_table():
    return """DELETE FROM {} WHERE {}_id = %s"""

def create_statements_block(request_data) -> tuple:
    parameters = []
    for key, value in request_data.items():
        parameters.append(value)
    return tuple(parameters)

def accomodate_data(mysql, request_data: dict) -> tuple: 
    corrected_data = {}
    
    for key, value in request_data.items():
        match(key):
            case "Category":
                corrected_data.update(get_category_id_by_name(mysql, value))
            case "Summary":
                corrected_data.update({"summary": "{}".format(value)})
            case _:
                corrected_data.update({key: value})
    return corrected_data
