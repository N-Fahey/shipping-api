from flask import Flask

from .db import db, DB_CONNSTR
from .controllers import cli_bp
from .routes import routes_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNSTR
    db.init_app(app)

    app.json.sort_keys = False

    @app.route('/')
    def index():
        return {'message': 'Hello, World!'}
    
    app.register_blueprint(cli_bp)
    app.register_blueprint(routes_bp)
    
    return app
    