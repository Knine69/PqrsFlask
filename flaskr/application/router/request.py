from flask import Blueprint, request, jsonify
from ..router.utils.utils import return_table_name
from ...domain.config import Config
from ...domain.models.queries.requestquery import Request
from ..security.tokenmanager import JwtManager

token_manager = JwtManager()
router_request = Blueprint('router_request', __name__, template_folder='templates', url_prefix='/request')
mysql = Config.give_mysql_instance(self=Config)

request_query = Request(return_table_name(router_request))

@router_request.route('/<int:id>', methods=["GET"])
@token_manager.jwt_required
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    return jsonify(request_query.get_single_registry(id))

@router_request.get('/')
@token_manager.jwt_required
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    return jsonify(request_query.get_registries(request))

@router_request.post("/new_request")
@token_manager.jwt_required
def insert_new_request():
    """
    Creates new request based on a received body sent from the Web Server
    """
    return jsonify(request_query.post_new(request))

@router_request.delete("/<int:id>")
@token_manager.jwt_required
def delete_request(id):
    """
    Deletes a specific request based on a given ID

    id: Given ID to delete in database
    """
    return jsonify(request_query.delete_registry(id))

@router_request.patch("/<int:id>")
@token_manager.jwt_required
def update_request(id):
    """
    Updates a request in database based on the received elements from a JSON coming from the Web Server
    """
    return jsonify(request_query.patch_registry(id, request))