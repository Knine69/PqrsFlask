from flask import Request
from .queryexecutor import QueryExecutor
from ....application.router.utils.utils import ERROR_MESSAGE, get_person_by_document_id
from ..sqlstatements import create_statements_block, create_new_person
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from .utils.secureutilities import SecurityConstants
import json, base64

class PersonQuery(QueryExecutor):

    __public_key= None
    __private_key= None

    def __init__(self, table_name) -> None:
        super().__init__(table_name)
        self.__utils = SecurityConstants()
        with open(self.__utils.get_secret_key_path(), 'r') as file:
            self.__private_key = file.read().strip()

        with open(self.__utils.get_public_key_path(), 'r') as file:
            self.__public_key = file.read().strip()

    def get_person_by_document(self, document):
        return get_person_by_document_id(self.mysql, document)["person"]

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

    def __encrypt_data(self, data: str):
        public_key = serialization.load_pem_public_key(self.__public_key.encode(), default_backend())

        encrypted_data = public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(encrypted_data).decode()

    def __decrypt_data(self, encrypted_data):
        private_key = serialization.load_pem_private_key(self.__private_key.encode(), str(self.__utils.get_secret()).encode(), default_backend())
        decrypted_data = private_key.decrypt(
            base64.b64decode(encrypted_data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_data.decode()