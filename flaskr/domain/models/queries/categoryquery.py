from .queryexecutor import QueryExecutor
from ....application.router.utils.utils import ERROR_MESSAGE
from ..sqlstatements import create_statements_block, create_new_category
import json

class Category(QueryExecutor):
    def __init__(self, table_name) -> None:
        super().__init__(table_name)

    def get_single_registry(self, id):
        return super().get_single_registry(id)
        
    def get_registries(self):
        return super().get_registries()
    
    def post_new(self, request):
        try:
            if super().validate_create_user_identity(request.headers.get("Authorization"),  request.headers.get("documentId")):
                request_data = json.loads(request.data.decode('utf-8'))
                with self.mysql.connection.cursor() as cur:
                    cur.execute(create_new_category(), create_statements_block(request_data))
                    self.mysql.connection.commit()
                    cur.close()
            else:
                return ERROR_MESSAGE.format("User is not ahutorized to perform this operation"), 401
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500

        return {"Response":"Insert successfull"}
    
    def delete_registry(self, id, request):
        result = super().validate_and_process_admin_operations(request)
        if  type(result) == dict:
            return result
        else:
            return super().delete_registry(id)
    
    
    def patch_registry(self, id, request):
        result = super().validate_and_process_admin_operations(request)
        if  type(result) == dict:
            return result
        else:
            return super().patch_registry(id, request) 