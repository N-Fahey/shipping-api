from flask import Flask

from .db import db, DB_CONNSTR
from .errors import register_error_handler
from .controllers import cli_bp
from .routes import routes_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNSTR
    db.init_app(app)

    app.json.sort_keys = False

    @app.route('/')
    def index():
        return {'status': 'healthy'}
    
    app.register_blueprint(cli_bp)
    app.register_blueprint(routes_bp)

    register_error_handler(app)
    
    return app
    