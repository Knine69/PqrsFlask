from flask import Flask
from flask_cors import CORS
from .domain.config import Config

from flask_mysqldb import MySQL
from flask_mail import Mail
from .application.router.category import router_category
from .application.router.department import router_department
from .application.router.person import router_person
from .application.router.position import router_position
from .application.router.request import router_request
from .application.router.role import router_role
from .application.router.state import router_state
from .application.router.login import router_login

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
mail = Mail(app)

app.register_blueprint(router_category)
app.register_blueprint(router_department)
app.register_blueprint(router_person)
app.register_blueprint(router_position)
app.register_blueprint(router_request)
app.register_blueprint(router_role)
app.register_blueprint(router_state)
app.register_blueprint(router_login)

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

if __name__ == "__main__":
    app.run(debug=True)
