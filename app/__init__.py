from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name='default'):
    """Crée et configure l'application Flask."""
    app = Flask(__name__)
    
    # Charger la configuration à partir de config.py
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialiser les extensions avec l'application
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return None

    # Importer et enregistrer les blueprints
    from .routes.clients import clients_bp
    app.register_blueprint(clients_bp)
    from .routes.rdv import rdv_bp
    app.register_blueprint(rdv_bp)

    with app.app_context():
        from .models import rdv, client

    return app