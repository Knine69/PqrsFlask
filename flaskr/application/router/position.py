from flask import Blueprint, request, jsonify
from ..router.utils.utils import return_table_name
from ...domain.config import Config
from ...domain.models.queries.positionquery import Position

router_position = Blueprint('router_position', __name__, template_folder='templates', url_prefix='/position')
mysql = Config.give_mysql_instance(self=Config)

position_query = Position(return_table_name(router_position))

@router_position.route('/<int:id>', methods=["GET"])
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    return jsonify(position_query.get_single_registry(id))

@router_position.get('/')
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    jsonify(position_query.get_registries())
    """
    Creates new position based on a received body sent from the Web Server
    """
    return jsonify(position_query.post_new(request))

@router_position.delete("/<int:id>")
def delete_position(id):
    """
    Deletes a specific position based on a given ID

    id: Given ID to delete in database
    """
    return jsonify(position_query.delete_registry(id))

def update_position(id):
    """
    Updates a position in database based on the received elements from a JSON coming from the Web Server
    """
    return jsonify(position_query.patch_registry(id, request))
