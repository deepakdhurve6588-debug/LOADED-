import logging
from fbchat import Client
from fbchat.models import *

logger = logging.getLogger(__name__)

class FacebookAPI:
    def __init__(self):
        self.client = None
    
    def login(self, appstate):
        """Login with appstate"""
        try:
            self.client = Client(session_cookies=appstate)
            logger.info("Logged in with appstate")
            return True
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def send_message(self, uid, message):
        """Send message"""
        try:
            self.client.send(Message(text=message), thread_id=uid)
            logger.info(f"Message sent to {uid}")
            return True
        except Exception as e:
            logger.error(f"Message sending error: {e}")
            return False
    
    def logout(self):
        """Logout"""
        if self.client:
            self.client.logout()
