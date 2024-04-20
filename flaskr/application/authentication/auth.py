from ..dto.user import UserDto
from ...domain.models.person import Person
from ...domain.models.queries.personquery import get_person_by_document_id
from ..security.tokenmanager import JwtManager

class AuthenticationManager():
    _mysql = None 
    _token_manager = None

    def __init__(self, mysql) -> None:
        self._token_manager = JwtManager()
        self._mysql = mysql
        
    def authenticate(self, request_data):
        user_dto = UserDto(request_data["document"], request_data["password"])
        person = Person(self._get_user_by_document(user_dto.get_document()))
        if self._login(user_dto.get_password(), self._token_manager._decrypt_data(person.get_password())):
            return {
                "Description":"Correctly authenticated",
                "validSession": True,
                "sessionToken": self._token_manager.generate_token(person)
                }
        return "Authentication failed" 
    
    def _get_user_by_document(self, document) -> dict: 
        response = get_person_by_document_id(self._mysql, document)["person"]
        return response if response else None
        
    def _login(self, dto_password, password):
        return self._compare_password(dto_password, password)

    def _compare_password(self, dto_password:str, password:str):
        return dto_password.lower() == password.lower()