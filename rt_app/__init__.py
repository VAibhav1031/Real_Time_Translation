from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from rt_app.config import get_config
from flask_migrate import Migrate

migrate = Migrate()
db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(get_config())
    db.init_app(app)
    migrate.init_app(app,db)

    csrf.init_app(app)   
    
    from rt_app.backend import main
    app.register_blueprint(main)
    return app 


