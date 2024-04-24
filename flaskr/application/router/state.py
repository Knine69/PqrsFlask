from flask import Blueprint, request, jsonify
from ..router.utils.utils import return_table_name
from ...domain.config import Config
from ...domain.models.queries.statequery import State
from ..security.tokenmanager import JwtManager

token_manager = JwtManager()
router_state = Blueprint('router_state', __name__, template_folder='templates', url_prefix='/state')
mysql = Config.give_mysql_instance(self=Config)

state_query = State(return_table_name(router_state), JwtManager())

@router_state.route('/<int:id>', methods=["GET"])
@token_manager.jwt_required
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    return jsonify(state_query.get_single_registry(id))
    
@router_state.get('/')
@token_manager.jwt_required
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    return jsonify(state_query.get_registries())

@router_state.post("/new_state")
@token_manager.jwt_required
def insert_new_state():
    """
    Creates new state based on a received body sent from the Web Server
    """
    return jsonify(state_query.post_new(request))

@router_state.delete("/<int:id>")
@token_manager.jwt_required
def delete_state(id):
    """
    Deletes a specific state based on a given ID

    id: Given ID to delete in database
    """
    return jsonify(state_query.delete_registry(id, request))

@router_state.patch("/<int:id>")
@token_manager.jwt_required
def update_state(id):
    """
    Updates a state in database based on the received elements from a JSON coming from the Web Server
    """
    return jsonify(state_query.patch_registry(id, request))
