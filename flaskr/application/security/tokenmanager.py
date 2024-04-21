from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify
from jose import jwt 
from jose.constants import ALGORITHMS 
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from ...domain.models.person import Person
from ...application.dto.user import UserDto
from ...domain.models.queries.utils.secureutilities import SecurityConstants

class JwtManager():
    __security_constants = SecurityConstants()
    def __init__(self) -> None:
        
        self.__utils = SecurityConstants()
        with open(self.__security_constants.get_secret_key_path(), 'rb') as file:
            self.__private_key = self.__decrypt_private_key(file.read())

        with open(self.__security_constants.get_public_key_path(), 'r') as file:
            self.__public_key = file.read().strip()

    def generate_token(self, user_details: Person):
        payload = {
            "documentId": user_details.get_document(),
            "email": user_details.get_email(),
            "role": user_details.get_role(),
            "position": user_details.get_position(),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=20)
        }
        pem_key = self.__private_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption())
        token = jwt.encode(payload, pem_key, algorithm=ALGORITHMS.RS256)
        return  token

    def jwt_required(self, f):
        @wraps(f)
        def validate_token(*args, **kwargs):
            try:
                token = request.headers.get("Authorization")
                user_dto =  UserDto(request.headers.get("documentId"), "")
                payload: dict = self.__decrypt_token(token)
                exp_datetime_utc:datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
                
                if self.__compare_credentials(payload.get("documentId"), user_dto.get_document()) and self.__verify_expiration_date(exp_datetime_utc):
                    print("Authorization Data is correct")
                    return f(*args, **kwargs)
                else:
                    return jsonify({"error": "Unauthorized"}), 401
            except Exception:
                print("Authorization data Incorrect")
                return jsonify({"error": "Unauthorized"}), 401
        
        return validate_token
    
    def _encrypt_data(self, data: str):
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

    def _decrypt_data(self, encrypted_data):
        decrypted_data = self.__private_key.decrypt(
            base64.b64decode(encrypted_data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_data.decode()
    
    def validate_user_consult_identity(self, token, document):
        payload: dict = self.__decrypt_token(token)
        return self.__compare_credentials(document, payload.get("documentId"))
        

    def __decrypt_token(self, token):
        return jwt.decode(token, self.__public_key, algorithms=[ALGORITHMS.RS256])

    def __decrypt_private_key(self, key):
        return serialization.load_pem_private_key(key, str(self.__utils.get_secret()).encode(), default_backend())
    
    def __compare_credentials(self, payload: str, document: str):
        return payload == document
    
    def __verify_expiration_date(self, exp_datetime_utc: datetime):
        return exp_datetime_utc > datetime.now(timezone.utc)