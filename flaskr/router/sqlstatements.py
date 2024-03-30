def get_one_from_table():
    return """SELECT * FROM {} where {}_id = %s"""

def get_all_entities():
    return """SELECT * FROM {}"""

def get_person_information():
    return """SELECT s.* FROM (select @person_id:= %s p) parm , LookUpPersonInformation s;"""

def get_request_information():
    return """SELECT s.* FROM (select @request_id:= %s p) parm , LookUpRequestInfo s;"""

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
    return """INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES (%s, %s, %s, %s, %s, %s)"""

def create_new_request():
    return """INSERT INTO request (generated_at, summary, category_id, requester_id) VALUES (%s, %s, %s, %s)"""

def delete_from_table():
    return """DELETE FROM {} WHERE {}_id = %s"""

def create_statements_block(request_data):
    parameters = []
    for key, value in request_data.items():
        parameters.append(value)
    return tuple(parameters)