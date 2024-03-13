from flask import Blueprint

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