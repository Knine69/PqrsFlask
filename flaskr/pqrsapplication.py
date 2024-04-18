from flask import Flask
from flask_cors import CORS
from .domain.config import Config
from .application.router.category import router_category
from .application.router.department import router_department
from .application.router.person import router_person
from .application.router.position import router_position
from .application.router.request import router_request
from .application.router.role import router_role
from .application.router.state import router_state

app = Flask(__name__)

app.register_blueprint(router_category)
app.register_blueprint(router_department)
app.register_blueprint(router_person)
app.register_blueprint(router_role)
app.register_blueprint(router_position)
app.register_blueprint(router_request)
app.register_blueprint(router_state)

app.config.from_object(Config)

mysql = Config.give_mysql_instance(self=Config)

mysql.init_app(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})