from .queryexecutor import QueryExecutor
from ....application.router.utils.utils import ERROR_MESSAGE
from ..sqlstatements import create_statements_block, create_new_request, get_person_requests, get_request_information
from ....application.router.utils.utils import get_person_id_by_document_id, get_person_by_document_id, get_category_id_by_name, give_new_request_body, get_state_by_id, get_person_by_id
from ....application.security.tokenmanager import JwtManager
from ..queries.personquery import PersonQuery
from ....domain.config import Config

from flask import Request
from flask_mail import Message

import json

class Request(QueryExecutor):
    def __init__(self, table_name, manager: JwtManager) -> None:
        super().__init__(table_name)
        self._person_query = PersonQuery(table_name)
        self._token_manager = manager
        self._mail = Config.give_mail_instance(self=Config)

    def get_single_registry(self, id, request):
        document = request.headers.get("documentId")
        validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, False)
        if validation["isAdmin"]:
            return super().get_single_registry(id)
        elif validation["userValidated"]:
            person_id = self._get_person_name(document)
            with self.mysql.connection.cursor() as cur:
                cur.execute(get_request_information(), (id, ))
                data = cur.fetchall()
                cur.close()
                return data if data[0]["Requester"] == person_id else (super().return_unauthorized_error() )
        else: 
            return super().return_unauthorized_error() 
        
    def get_registries(self, request):
        try:
            document = request.headers.get("documentId")
            validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, False)
            if validation["isAdmin"]:
                return super().get_registries()
            elif validation["userValidated"]:
                return self._get_user_requests(document)
            else:
                return super().return_unauthorized_error() 
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500

    
    def post_new(self, request: Request):
        try:
            if super().validate_create_user_identity(request.headers.get("Authorization"),  request.headers.get("documentId"), False):
                request_data = self._adapt_request_data_new_request(request)
                if not request_data["error"]:
                    with self.mysql.connection.cursor() as cur:
                        cur.execute(create_new_request(), create_statements_block(give_new_request_body(request_data)))
                        self.mysql.connection.commit()
                        cur.close()
                return {       
                    "Description": "Insert successfull"
                    }
            else:
                return ERROR_MESSAGE.format("User is not ahutorized to perform this operation"), 401
        except Exception as e:
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
    
    def delete_registry(self, id, request):
        try:
            document = request.headers.get("documentId")
            validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, False)
            if validation["isAdmin"]:
                return super().delete_registry(id)
            elif validation["userValidated"]:
                if self._validate_ownership(id, document):
                    return super().delete_registry(id)
                else:
                    return super().return_unauthorized_error() 
            else:
                return super().return_unauthorized_error() 
        except Exception as e: 
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
    
    def patch_registry(self, id, request: Request):
        try:
            document = request.headers.get("documentId")
            state_now_name, state_after_name, send_to_email = self._prepare_email_info(id, request)
            validation = self._token_manager.validate_user_consult_identity(request.headers.get("Authorization"), document, False)
            if validation["isAdmin"]:
                response = super().patch_registry(id, request) 
                if state_now_name:
                    self.send_email(send_to_email, state_now_name, state_after_name, id)
                return response
            elif validation["userValidated"]:
                if self._validate_ownership(id, document):
                    response = super().patch_registry(id, request) 
                    if state_now_name:
                        self.send_email(send_to_email, state_now_name, state_after_name, id)
                    return response 
                else:
                    return super().return_unauthorized_error() 
            else:
                return super().return_unauthorized_error() 
        except Exception as e: 
            error_message = ERROR_MESSAGE.format(str(e))
            return error_message, 500
        
    def _validate_ownership(self, id, document):
        return any(item["RequestId"] == id for item in self._get_user_requests(document))

    def _get_user_requests(self, document):
        person_id = self._get_person(document)["person_id"]
        with self.mysql.connection.cursor() as cur:
            cur.execute(get_person_requests(), (person_id, ))
            data = cur.fetchall()
            cur.close()
            return data 
    
    def _adapt_request_data_new_request(self, request: Request):
        request_data: dict = json.loads(request.data.decode('utf-8'))
        request_data.update(self._get_category(request_data.get("category")))
        request_data.update(self._get_person(request.headers.get("documentId")))
        request_data.pop("category")
        return request_data
    
    def _get_category(self, data):
        return get_category_id_by_name(self.mysql, data)

    def _get_person(self, data):
        return get_person_id_by_document_id(self.mysql, data)
    
    def _get_person_name(self, data):
        return get_person_by_document_id(self.mysql, data)["person"]["name"]
    
    def _prepare_email_info(self, id, request):
        state_now: dict = self.get_single_registry(id, request)[0]
        
        received_body = json.loads(request.data.decode('utf-8'))
        
        if received_body.get("state_id"):
            state_now_name = get_state_by_id(self.mysql, state_now.get("state_id")).get("state")
            state_after_name = get_state_by_id(self.mysql, received_body.get("state_id")).get("state")
            requester_email = get_person_by_id(self.mysql, state_now.get("requester_id")).get("email")

            return (state_now_name, state_after_name, requester_email)
        
        return (None, None, None)

    def send_email(self, to_email, state_before, state_now, request_id): 
        msg = Message("Actualización de PQRS: {}".format(request_id),
                  recipients=[to_email],
                  body="Tu solicitud se ha actualizado: {} -> {} - Para usuario: {}".format(state_before, state_now, to_email))
        self._mail.send(msg)
    