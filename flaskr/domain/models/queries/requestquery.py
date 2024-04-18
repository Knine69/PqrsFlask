from .queryexecutor import QueryExecutor
from ....application.router.utils.utils import ERROR_MESSAGE
from ..sqlstatements import create_statements_block, create_new_request
from ....application.router.utils.utils import get_person_id_by_document_id, get_category_id_by_name, give_new_request_body
import json

class Request(QueryExecutor):
    def __init__(self, table_name) -> None:
        super().__init__(table_name)

    def get_single_registry(self, id):
        return super().get_single_registry(id)
        
    def get_registries(self):
        return super().get_registries()
    
    def post_new(self, request):
        try:
            request_data = self._adapt_request_data_new_request(request)
            if not request_data["error"]:
                with self.mysql.connection.cursor() as cur:
                    cur.execute(create_new_request(), create_statements_block(give_new_request_body(request_data)))
                    self.mysql.connection.commit()
                    cur.close()
                    return {       
                        "Description": "Insert successfull"
                        }
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
    
    def delete_registry(self, id):
        return super().delete_registry(id)
    
    
    def patch_registry(self, id, request):
        return super().patch_registry(id, request)
    
    def _adapt_request_data_new_request(self, request):
        request_data = json.loads(request.data.decode('utf-8'))
        request_data.update(self._get_category(request_data["category"]))
        request_data.update(self._get_person(request_data["documentId"]))

        request_data.pop("category")
        request_data.pop("documentId")
        return request_data

    def _get_category(self, data):
        return get_category_id_by_name(self.mysql, data)

    def _get_person(self, data):
        return get_person_id_by_document_id(self.mysql, data)

    
    