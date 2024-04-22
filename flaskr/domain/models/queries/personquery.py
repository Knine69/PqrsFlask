from flask import Request
from .queryexecutor import QueryExecutor
from ....application.router.utils.utils import ERROR_MESSAGE, get_person_by_document_id, get_role_by_id, get_position_by_id
from ..sqlstatements import create_statements_block, create_new_person
from ....application.security.tokenmanager import JwtManager
import json

class PersonQuery(QueryExecutor):
    def __init__(self, table_name) -> None:
        super().__init__(table_name)

    def get_person_by_document(self, document):
        bare_person: dict = get_person_by_document_id(self.mysql, document)["person"]
        return self._adapt_person(bare_person)

    def get_single_registry(self, id):
        return super().get_single_registry(id)
        
    def get_registries(self):
        return super().get_registries()
    
    def post_new(self, request: Request):
        try:
            ##Check how to receive encrypted data from front and save password in db encrypted - Temporary encryption
            if super().validate_create_user_identity(request.headers.get("Authorization"),  request.headers.get("documentId")):
                request_data = self._modify_user(request)
                with self.mysql.connection.cursor() as cur:
                    cur.execute(create_new_person(), create_statements_block(request_data))
                    self.mysql.connection.commit()
                    cur.close()
            else:
                return ERROR_MESSAGE.format("User is not ahutorized to perform this operation"), 401
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500

        return {"Response":"Insert successfull"}
    
    def delete_registry(self, id):
        return super().delete_registry(id)
    
    
    def patch_registry(self, id, request):
        return super().patch_registry(id, request)
    
    def _modify_user(self, request):
        manager = JwtManager()
        request_data: dict = json.loads(request.data.decode('utf-8'))
        password = request_data.get("password")
        request_data.pop("password")
        request_data.update({"password": manager._encrypt_data(password)})

        return request_data

    def _adapt_person(self, person: dict):
        transformed = person
        transformed.update(get_role_by_id(self.mysql, person.get("role_id")))
        transformed.update(get_position_by_id(self.mysql, person.get("position_id")))
        transformed.pop("position_id")
        transformed.pop("role_id")
        return transformed

