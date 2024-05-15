from flask import Request
from .queryexecutor import QueryExecutor
from ....application.router.utils.utils import *
from ..sqlstatements import create_statements_block, create_new_person, get_one_from_table
from ....application.security.tokenmanager import JwtManager
import json

class PersonQuery(QueryExecutor):
    def __init__(self, table_name) -> None:
        super().__init__(table_name)
        self._token_manager = JwtManager()

    def get_person_by_document(self, document):
        bare_person: dict = get_person_by_document_id(self.mysql, document)["person"]
        return self._adapt_person(bare_person)

    def get_single_registry(self, id, request):
        try:
            document = request.headers.get("documentId")
            validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, False)
            if validation["isAdmin"]:
                return super().get_single_registry(id)
            elif validation["userValidated"]:
                person_id = self._get_person(document)["person_id"]
                with self.mysql.connection.cursor() as cur:
                    cur.execute(get_one_from_table().format(self.table_name, self.table_name), create_statements_block({"id": person_id}))
                    data = cur.fetchall()
                    cur.close()
                    return data if data[0]["person_id"] == person_id else ({"Error": "Unauthorized"}, 401)
            else: 
                return {"Error": "Unauthorized"}, 401
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
        
    def get_registries(self, request):
        try:
            document = request.headers.get("documentId")
            validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, True)
            if validation["isAdmin"]:
                return super().get_registries()
            else:
                return {"Error": "Unauthorized"}, 401
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
    
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
    
    def sign_up(self, request: Request):
        try:
            request_data: dict = self._adapt_request_data_new_person(request)
            with self.mysql.connection.cursor() as cur:
                cur.execute(create_new_person(), create_statements_block(request_data))
                self.mysql.connection.commit()
                cur.close()
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500

        return {"Response":"Insert successfull"}
    
    def delete_registry(self, id, request):
        try:
            document = request.headers.get("documentId")
            validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, False)
            if validation["isAdmin"]:
                return super().delete_registry(id)
            elif validation["userValidated"]:
                if self._validate_ownership(id, request):
                    return super().delete_registry(id)
                else:
                    return super().return_unauthorized_error()
            else:
                return super().return_unauthorized_error()
        except Exception as e: 
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
    
    
    def patch_registry(self, id, request):
        try:
            document = request.headers.get("documentId")
            validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, False)
            if validation["isAdmin"]:
                return super().patch_registry(id, request)
            elif validation["userValidated"]:
                if self._validate_ownership(id, request):
                     return super().patch_registry(id, request)
                else:
                    return super().return_unauthorized_error()
            else:
                return super().return_unauthorized_error()
        except Exception as e: 
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
    
    def _validate_ownership(self, id, request):
        response = self.get_single_registry(id, request)[0]
        if "Error" in response:
            return False
        else:
            return response["person_id"] == id 
    
    def _modify_user(self, request):
        request_data: dict = json.loads(request.data.decode('utf-8'))
        manager = JwtManager()

        return self._password_encrypt(request_data, manager)

    def _password_encrypt(self, request: dict, manager: JwtManager):
        aux_request = request
        password = aux_request.get("password")
        aux_request.pop("password")
        aux_request.update({"password": manager._encrypt_data(password)})

        return aux_request
    
    def _adapt_person(self, person: dict):
        transformed = person
        transformed.update(get_role_by_id(self.mysql, person.get("role_id")))
        transformed.update(get_position_by_id(self.mysql, person.get("position_id")))
        transformed.pop("position_id")
        transformed.pop("role_id")
        return transformed

    def _get_person(self, data):
        return get_person_id_by_document_id(self.mysql, data)
    
    def _get_role(self, data):
        return get_role_id_by_name(self.mysql, data)
    
    def _get_position(self, data):
        return get_position_id_by_name(self.mysql, data)
    
    def _get_department(self, data):
        return get_department_id_by_name(self.mysql, data)
    
    def _adapt_request_data_new_person(self, request: Request):
        request_data: dict = json.loads(request.data.decode('utf-8'))
        
        request_data.update(self._get_role(request_data.get("role")))
        request_data.update(self._get_position(request_data.get("position")))
        request_data.update(self._get_department(request_data.get("department")))
        request_data.update({'document_id': request_data.get("documentId")})
        
        request_data.pop("role")
        request_data.pop("documentId")
        request_data.pop("position")
        request_data.pop("department")

        return {
            'name': request_data.get("name"),
            'document_id': request_data.get("document_id"),
            'email': request_data.get("email"),
            'position_id': request_data.get("position_id"),
            'role_id': request_data.get("role_id"),
            'department_id': request_data.get("department_id"),
            'password': request_data.get("password"),
        }
    
