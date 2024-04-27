from ..dto.user import UserDto
from ...domain.models.person import Person
from ...domain.models.queries.personquery import PersonQuery
from ..security.tokenmanager import JwtManager

class AuthenticationManager():
    _token_manager = None
    _person_query = None

    def __init__(self) -> None:
        self._token_manager = JwtManager()
        self._person_query = PersonQuery(table_name='person')
        
    def authenticate(self, request_data):
        user_dto = UserDto(request_data["document"], request_data["password"])
        person = Person(self._get_user_by_document(user_dto.get_document()))
        if self._login(self._token_manager._decrypt_data(user_dto.get_password()), self._token_manager._decrypt_data(person.get_password())):
            return {
                "description":"Correctly authenticated",
                "validSession": True,
                "sessionToken": self._token_manager.generate_token(person)
                }
        return {"description": "Authentication error", "code": 401, "validSession": False }
    
    def _get_user_by_document(self, document) -> dict: 
        response = self._person_query.get_person_by_document(document)
        return response if response else None
        
    def _login(self, dto_password, password):
        return self._compare_password(dto_password, password)

    def _compare_password(self, dto_password:str, password:str):
        return dto_password.lower() == password.lower()