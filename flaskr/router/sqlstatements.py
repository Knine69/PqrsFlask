def get_one_from_table():
    return """SELECT * FROM {} where {}_id = %s"""

def get_all_entities():
    return """SELECT * FROM {}"""

def create_new_role():
    return """INSERT INTO role (name) VALUES (%s)"""

def create_new_person():
    return """INSERT INTO person (name, document_id, email, position_id, role_id, department_id) VALUES (%s, %s, %s, %s, %s, %s)"""

def create_statements_block(request_data):
    parameters = []
    for key, value in request_data.items():
        parameters.append(value)
    return tuple(parameters)