from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

