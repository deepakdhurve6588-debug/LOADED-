from flask import Flask
import os
from .utils import setup_logging

def create_app():
    app = Flask(__name__)
    
    # Setup logging
    setup_logging()
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # Register blueprints
    from app.bot import bot_bp
    app.register_blueprint(bot_bp)
    
    return app
