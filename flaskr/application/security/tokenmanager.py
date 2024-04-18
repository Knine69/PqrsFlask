from datetime import datetime, timedelta, timezone
from ...domain.models.person import Person
from ...application.dto.user import UserDto
from jose import jwt
from jose.constants import ALGORITHMS

SECRET_KEY_PATH = "application/security/rsa/private_key.key"
PUBLIC_KEY_PATH = "application/security/rsa/public_key.key"

class JwtManager():
    __secret_key = None
    __public_key = None
    def __init__(self) -> None:
        with open(SECRET_KEY_PATH, 'r') as file:
            self.__secret_key = file.read().strip()

        with open(PUBLIC_KEY_PATH, 'r') as file:
            self.__public_key = file.read().strip()

    def generate_token(self, user_details: Person):
        self.__get_secret_key()

        payload = {
            "documentId": user_details.get_document(),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=20)
        }

        return jwt.encode(payload, self.__secret_key, algorithm=ALGORITHMS.RS256)

    def validate_token(self, user_dto:UserDto, token):
        payload = jwt.decode(token, self.__public_key, algorithms=[ALGORITHMS.RS256])

        if payload["documentId"] == user_dto.get_document():
            return payload

        return "You're not who you say you are!"

    def __get_secret_key(self):
        return self.__secret_key