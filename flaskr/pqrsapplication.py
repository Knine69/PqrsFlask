from flask import Flask
from domain.config import Config
from router.pqrsrouting import router, mysql

app = Flask(__name__)
app.register_blueprint(router)
app.config.from_object(Config)
mysql.init_app(app)