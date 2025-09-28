import os
import json
import base64
import logging
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import scrypt

logger = logging.getLogger(__name__)

class E2EEManager:
    def __init__(self, keys_dir="data/keys"):
        self.keys_dir = keys_dir
        os.makedirs(keys_dir, exist_ok=True)
        self.symmetric_key_path = os.path.join(keys_dir, "symmetric_key.key")
    
    def generate_symmetric_key(self, password):
        """Generate symmetric key"""
        try:
            salt = get_random_bytes(32)
            key = scrypt(password, salt, 32, N=2**14, r=8, p=1)
            
            key_data = {
                'key': base64.b64encode(key).decode('utf-8'),
                'salt': base64.b64encode(salt).decode('utf-8')
            }
            
            with open(self.symmetric_key_path, 'w') as f:
                json.dump(key_data, f)
            
            logger.info("Symmetric key generated")
            return True
        except Exception as e:
            logger.error(f"Error generating key: {e}")
            return False
    
    def encrypt_message(self, message):
        """Encrypt message"""
        try:
            with open(self.symmetric_key_path, 'r') as f:
                key_data = json.load(f)
            
            key = base64.b64decode(key_data['key'])
            iv = get_random_bytes(16)
            
            cipher = AES.new(key, AES.MODE_GCM, iv)
            encrypted_message, tag = cipher.encrypt_and_digest(message.encode('utf-8'))
            
            return {
                "success": True,
                "encrypted_message": base64.b64encode(encrypted_message).decode('utf-8'),
                "iv": base64.b64encode(iv).decode('utf-8'),
                "tag": base64.b64encode(tag).decode('utf-8'),
                "algorithm": "AES-GCM"
            }
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return {"success": False, "error": str(e)}
    
    def decrypt_message(self, encrypted_data):
        """Decrypt message"""
        try:
            with open(self.symmetric_key_path, 'r') as f:
                key_data = json.load(f)
            
            key = base64.b64decode(key_data['key'])
            encrypted_message = base64.b64decode(encrypted_data['encrypted_message'])
            iv = base64.b64decode(encrypted_data['iv'])
            tag = base64.b64decode(encrypted_data['tag'])
            
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted_message = cipher.decrypt_and_verify(encrypted_message, tag)
            
            return decrypted_message.decode('utf-8')
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return ""
