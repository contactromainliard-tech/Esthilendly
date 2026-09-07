from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Nom de la vue de connexion

def create_app(config_name='default'):
    """Crée et configure l'application Flask."""
    app = Flask(__name__)
    
    # Charger la configuration à partir de config.py
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialiser les extensions avec l'application
    db.init_app(app)
    
    # Importer et enregistrer les blueprints
    #from .routes import main as main_blueprint
    #app.register_blueprint(main_blueprint)

    # Configurer Flask-Migrate
    migrate.init_app(app, db)

    # Configurer Flask-Login
    login_manager.init_app(app)


    return app