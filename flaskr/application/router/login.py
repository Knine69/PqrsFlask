from flask import Blueprint, request
from ...domain.models.queries.personquery import PersonQuery
from ...application.authentication.auth import AuthenticationManager
from ...domain.config import Config
from ...application.dto.user import UserDto
import json

router_login = Blueprint('router_login', __name__, template_folder='templates', url_prefix='/login')
person_query = PersonQuery('person')
mysql = Config.give_mysql_instance(self=Config)

@router_login.post("/auth")
def login():
    request_data = json.loads(request.data.decode('utf-8'))
    auth_manager = AuthenticationManager(mysql)
    return auth_manager.authenticate(request_data)

@router_login.get("/test")
def test_validation():
    request_data = json.loads(request.data.decode('utf-8'))
    request_headers = request.headers.get("sessionToken", "empty")
    auth_manager = AuthenticationManager(mysql)
    
    return auth_manager.authorize_operation(request_data, request_headers)