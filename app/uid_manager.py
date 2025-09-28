import json
import os
import logging

logger = logging.getLogger(__name__)

class UIDManager:
    def __init__(self, uid_file="data/uids.txt"):
        self.uid_file = uid_file
        os.makedirs(os.path.dirname(uid_file), exist_ok=True)
    
    def save_uid(self, name, uid):
        """Save UID to file"""
        try:
            uids = self.load_all_uids()
            uids[name] = uid
            
            with open(self.uid_file, 'w') as f:
                json.dump(uids, f, indent=2)
            
            logger.info(f"UID saved for {name}: {uid}")
            return True
        except Exception as e:
            logger.error(f"Error saving UID: {e}")
            return False
    
    def load_all_uids(self):
        """Load all UIDs"""
        try:
            if os.path.exists(self.uid_file):
                with open(self.uid_file, 'r') as f:
                    return json.load(f)
            return {}
        except:
            return {}
    
    def get_uid(self, name):
        """Get UID for name"""
        uids = self.load_all_uids()
        return uids.get(name, "")
