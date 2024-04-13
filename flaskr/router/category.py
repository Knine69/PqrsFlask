from flask import Blueprint, request, jsonify
from ..router.utils.utils import return_table_name
from ..domain.config import Config
from ..domain.models.queries.categoryquery import Category

router_category = Blueprint('router_category', __name__, template_folder='templates', url_prefix='/category')
mysql = Config.give_mysql_instance(self=Config)

category_query = Category(return_table_name(router_category))

@router_category.route('/<int:id>', methods=["GET"])
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    return jsonify(category_query.get_single_registry(id))

@router_category.get('/')
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    return jsonify(category_query.get_registries())

@router_category.post("/new_category")
def insert_new_category():
    """
    Creates new category based on a received body sent from the Web Server
    """
    return jsonify(category_query.post_new(request))

@router_category.delete("/<int:id>")
def delete_category(id):
    """
    Deletes a specific category based on a given ID

    id: Given ID to delete in database
    """
    return jsonify(category_query.delete_registry(id))


@router_category.patch("/<int:id>")
def update_category(id):
    """
    Updates a category in database based on the received elements from a JSON coming from the Web Server
    """
    return jsonify(category_query.patch_registry(id, request))