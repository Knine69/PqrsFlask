from flask import Blueprint

PATCH_STORED_PROCEDURE = 'PatchRecordsInTable'

def fetch_resources(cur):

    main_result = cur.fetchall()
    remaining_result_sets = []
    while cur.nextset():
        remaining_result_sets.append(cur.fetchall())

    return [main_result, remaining_result_sets] 

def passdown_empty():
    return {
            "logged" : True,
            "table_information" : False,
            "response_table" : None,
            "table_name" : None

        }

def passdown_response(logged, table_info, response_table, table_name):
    return {
            "logged" : logged,
            "table_information" : table_info,
            "response_table" : response_table,
            "table_name" : table_name
        }

def _is_logged():
    return True

def return_table_name(router: Blueprint):
    return router.url_prefix[1:]