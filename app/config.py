import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        # Facebook credentials
        self.email = os.getenv('FB_EMAIL', '')
        self.password = os.getenv('FB_PASSWORD', '')
        self.user_id = os.getenv('FB_USER_ID', '')
        
        # Friend information
        self.deepak_uid = os.getenv('DEEPAK_UID', '')
        self.deepak_name = os.getenv('DEEPAK_NAME', 'Deepak kumar kumar')
        
        # E2EE settings
        self.enable_e2ee = os.getenv('ENABLE_E2EE', 'true').lower() == 'true'
        self.encryption_algorithm = os.getenv('ENCRYPTION_ALGORITHM', 'AES')
        self.key_size = int(os.getenv('KEY_SIZE', '256'))
        
        # File paths
        self.appstate_file = os.getenv('APPSTATE_FILE', 'data/appstate.json')
        self.uid_file = os.getenv('UID_FILE', 'data/uids.txt')
        self.secret_conversations_dir = os.getenv('SECRET_CONVERSATIONS_DIR', 'data/secret_conversations')
        self.keys_dir = os.getenv('KEYS_DIR', 'data/keys')
        
        # Bot settings
        self.message_delay = int(os.getenv('MESSAGE_DELAY', '3'))
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        self.headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        
        self._validate_config()
    
    def _validate_config(self):
        """Validate configuration"""
        if not self.email or not self.password:
            raise ValueError("FB_EMAIL and FB_PASSWORD must be set in environment variables")
    
    def get_messages(self):
        """Get default messages"""
        return [
            "Hello Deepak! 👋",
            "Ye E2EE encrypted message hai",
            "End-to-end encryption active 🔐",
            "Secure communication! 🎉",
            "Goodbye! 😊"
        ]
