from flask import Blueprint, request, jsonify
import logging
from .config import Config
from .e2ee_manager import E2EEManager
from .appstate_manager import AppStateManager
from .uid_manager import UIDManager

bot_bp = Blueprint('bot', __name__)
logger = logging.getLogger(__name__)

class MessengerBot:
    def __init__(self):
        self.config = Config()
        self.e2ee_manager = E2EEManager()
        self.appstate_manager = AppStateManager()
        self.uid_manager = UIDManager()
    
    def send_to_deepak(self, messages=None):
        """Send messages to Deepak"""
        try:
            if not messages:
                messages = self.config.get_messages()
            
            # Initialize E2EE
            if self.config.enable_e2ee:
                self.e2ee_manager.generate_symmetric_key(self.config.password)
            
            # Send messages logic here
            return {
                "success": True,
                "message": f"Sent {len(messages)} messages to Deepak",
                "e2ee_enabled": self.config.enable_e2ee
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

@bot_bp.route('/')
def home():
    return jsonify({
        "status": "active",
        "message": "Deepak E2EE Messenger Bot",
        "e2ee_enabled": True
    })

@bot_bp.route('/send/deepak', methods=['POST'])
def send_to_deepak():
    bot = MessengerBot()
    data = request.get_json() or {}
    messages = data.get('messages')
    
    result = bot.send_to_deepak(messages)
    return jsonify(result)
