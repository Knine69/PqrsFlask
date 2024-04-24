from flask import Blueprint, request, jsonify
from ..router.utils.utils import return_table_name
from ...domain.config import Config
from ...domain.models.queries.rolequery import Role
from ..security.tokenmanager import JwtManager

token_manager = JwtManager()
router_role = Blueprint('router_role', __name__, template_folder='templates', url_prefix='/role')
mysql = Config.give_mysql_instance(self=Config)

role_query = Role(return_table_name(router_role))

@router_role.route('/<int:id>', methods=["GET"])
@token_manager.jwt_required
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    return jsonify(role_query.get_single_registry(id))

@router_role.get('/')
@token_manager.jwt_required
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    return jsonify(role_query.get_registries())

@router_role.post("/new_role")
@token_manager.jwt_required
def insert_new_role():
    """
    Creates new role based on a received body sent from the Web Server
    """
    return jsonify(role_query.post_new(request))

@router_role.delete("/<int:id>")
@token_manager.jwt_required
def delete_role(id):
    """
    Deletes a specific role based on a given ID

    id: Given ID to delete in database
    """
    return jsonify(role_query.delete_registry(id, request))

@router_role.patch("/<int:id>")
@token_manager.jwt_required
def update_role(id):
    """
    Updates a request in database based on the received elements from a JSON coming from the Web Server
    """
    return jsonify(role_query.patch_registry(id, request))
