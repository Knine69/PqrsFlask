from ..dto.user import UserDto
from ...domain.models.queries.personquery import get_person_by_document_id
from ...domain.models.person import Person
class AuthenticationManager():
    _mysql = None 

    def __init__(self, mysql) -> None:
        self._mysql = mysql
        
    def authenticate(self, request_data):
        user_dto = UserDto(request_data["document"], request_data["password"])
        person = Person(self._get_user_by_document(user_dto.get_document()))
        if self._login(user_dto.get_password(), person.get_password()):
            return "Correctly authenticated"
        return "Authentication failed" 

    def authorize_operation(self, user_dto, token):
        return self._validate_credentials(user_dto, token)
    

    def _get_user_by_document(self, document) -> dict: 
        response = get_person_by_document_id(self._mysql, document)["person"]
        return response if response else None
        
    def _validate_credentials(self, user_dto, token) -> bool:
        # Check case for JWT validation
        return 

    def _login(self, dto_password, password):
        return self._compare_password(dto_password, password)

    def _compare_password(self, dto_password:str, password:str):
        return dto_password.lower() == password.lower()