import logging
import os
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, 'bot.log')),
            logging.FileHandler(os.path.join(log_dir, 'e2ee.log')),
            logging.StreamHandler()
        ]
    )

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()

def create_directories():
    """Create necessary directories"""
    directories = [
        'data',
        'data/secret_conversations',
        'data/keys',
        'logs',
        'templates',
        'static/css',
        'static/js',
        'static/images',
        'scripts',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("✅ All directories created successfully")
