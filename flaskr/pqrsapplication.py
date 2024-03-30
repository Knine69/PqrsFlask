from flask import Flask
from flask_cors import CORS
from .domain.config import Config
from .router.category import router_category
from .router.department import router_department
from .router.person import router_person
from .router.position import router_position
from .router.request import router_request
from .router.role import router_role
from .router.state import router_state

app = Flask(__name__)

app.register_blueprint(router_category)
app.register_blueprint(router_department)
app.register_blueprint(router_person)
app.register_blueprint(router_role)
app.register_blueprint(router_position)
app.register_blueprint(router_request)
app.register_blueprint(router_state)

app.config.from_object(Config)

mysql = Config.give_mysql_instance()
mysql.init_app(app)
CORS(app)