from flask import Blueprint, request, jsonify
from ..domain.models.sqlstatements import get_person_information, create_statements_block, get_all_entities, delete_from_table, create_new_person
from ..router.utils.utils import return_table_name, PATCH_STORED_PROCEDURE, fetch_resources, ERROR_MESSAGE
from ..domain.config import Config
from ..domain.models.queries.personquery import Person
import json

router_person = Blueprint('router_person', __name__, template_folder='templates', url_prefix='/person')
mysql = Config.give_mysql_instance(self=Config)

person_query = Person(return_table_name(router_person))

@router_person.route('/<int:id>', methods=["GET"])
def get_single_entry(id):
    """
    Brings a specific registry from a specific table dynamically.

    id: Gives the specific ID to look for in the database
    """
    return jsonify(person_query.get_single_registry(id))

@router_person.get('/')
def get_all():
    """
    Brings a all entries from a specific table dynamically.
    """
    return jsonify(person_query.get_registries())

@router_person.post("/new_person")
def insert_new_person():
    """
    Creates new person based on a received body sent from the Web Server
    """
    return jsonify(person_query.post_new(request))

@router_person.delete("/<int:id>")
def delete_person(id):
    """
    Deletes a specific person based on a given ID

    id: Given ID to delete in database
    """
    return jsonify(person_query.delete_registry(id))

@router_person.patch("/<int:id>")
def update_personrouter_person(id):
    """
    Updates a person in database based on the received elements from a JSON coming from the Web Server
    """
    return jsonify(person_query.patch_registry(id, request))
