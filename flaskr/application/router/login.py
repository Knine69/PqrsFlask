from flask import Blueprint, request, jsonify
from ...domain.models.queries.personquery import PersonQuery
from ...application.authentication.auth import AuthenticationManager
from ...domain.config import Config
import json

router_login = Blueprint('router_login', __name__, template_folder='templates', url_prefix='/login')
person_query = PersonQuery('person')
mysql = Config.give_mysql_instance(self=Config)

@router_login.post("/auth")
def login():
    request_data = json.loads(request.data.decode('utf-8'))
    auth_manager = AuthenticationManager()
    return jsonify(auth_manager.authenticate(request_data))