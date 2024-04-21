from flask import Request
from .queryexecutor import QueryExecutor
from ....application.router.utils.utils import ERROR_MESSAGE, get_person_by_document_id, get_role_by_id, get_position_by_id
from ..sqlstatements import create_statements_block, create_new_person
import json

class PersonQuery(QueryExecutor):
    def __init__(self, table_name) -> None:
        super().__init__(table_name)

    def get_person_by_document(self, document):
        bare_person: dict = get_person_by_document_id(self.mysql, document)["person"]
        return self._adapt_person(bare_person)

    def _adapt_person(self, person: dict):
        transformed = person
        transformed.update(get_role_by_id(self.mysql, person.get("role_id")))
        transformed.update(get_position_by_id(self.mysql, person.get("position_id")))
        transformed.pop("position_id")
        transformed.pop("role_id")
        return transformed

    def get_single_registry(self, id):
        return super().get_single_registry(id)
        
    def get_registries(self):
        return super().get_registries()
    
    def post_new(self, request: Request):
        try:
            ##Check how to receive encrypted data from front and save password in db encrypted
            request_data = json.loads(request.data.decode('utf-8'))
            with self.mysql.connection.cursor() as cur:
                cur.execute(create_new_person(), create_statements_block(request_data))
                self.mysql.connection.commit()
                cur.close()
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500

        return {"Response":"Insert successfull"}
    
    def delete_registry(self, id):
        return super().delete_registry(id)
    
    
    def patch_registry(self, id, request):
        return super().patch_registry(id, request)
