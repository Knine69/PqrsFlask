from flask import Blueprint, request, jsonify
from ..router.utils.utils import return_table_name
from ...domain.models.queries.departmentquery import Department

router_department = Blueprint('router_department', __name__, template_folder='templates', url_prefix='/department')
deparment_query = Department(return_table_name(router_department))

@router_department.route('/<int:id>', methods=["GET"])
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    return jsonify(deparment_query.get_single_registry(id))

@router_department.get('/')
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    return jsonify(deparment_query.get_registries(id))

@router_department.post("/new_department")
def insert_new_department():
    """
    Creates new department based on a received body sent from the Web Server
    """
    return jsonify(deparment_query.post_new(request))

@router_department.delete("/<int:id>")
def delete_department(id):
    """
    Deletes a specific department based on a given ID

    id: Given ID to delete in database
    """
    return jsonify(deparment_query.delete_registry(id))

@router_department.patch("/<int:id>")
def update_department(id):
    """
    Updates a department in database based on the received elements from a JSON coming from the Web Server
    """
    return jsonify(deparment_query.patch_registry(id, request))
