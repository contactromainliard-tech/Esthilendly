import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de base pour l'application Flask."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'une-chaine-aleatoire-a-changer')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Configuration spécifique à l'environnement de développement."""
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': Config
}