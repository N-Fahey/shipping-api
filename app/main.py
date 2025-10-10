from flask import Flask

from .db import db, DB_CONNSTR
from .controllers import cli_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNSTR
    db.init_app(app)

    @app.route('/')
    def index():
        return {'message': 'Hello, World!'}
    
    app.register_blueprint(cli_bp)
    
    return app
    