from flask import Flask

from .db import db, DB_CONNSTR

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNSTR
    db.init_app(app)

    @app.route('/')
    def index():
        return {'message': 'Hello, World!'}
    
    print('Server started')
    return app
    