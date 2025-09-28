import os
import json
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)

class SecretConversationManager:
    def __init__(self, appstate_manager, data_dir="data/secret_conversations"):
        self.appstate_manager = appstate_manager
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def enable_secret_conversation(self, friend_uid, friend_name):
        """Enable secret conversation"""
        try:
            appstate = self.appstate_manager.load_appstate()
            if not appstate:
                return False
            
            driver = webdriver.Chrome()
            
            try:
                driver.get("https://facebook.com")
                for cookie in appstate:
                    driver.add_cookie({
                        'name': cookie['name'],
                        'value': cookie['value'],
                        'domain': cookie.get('domain', '.facebook.com')
                    })
                
                driver.get("https://messenger.com")
                time.sleep(5)
                
                # Search and enable secret conversation
                search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search Messenger']")
                search_box.send_keys(friend_name)
                time.sleep(3)
                
                friend_element = driver.find_element(By.XPATH, f"//span[contains(text(), '{friend_name}')]")
                friend_element.click()
                time.sleep(3)
                
                # Save secret info
                secret_info = {
                    "friend_uid": friend_uid,
                    "friend_name": friend_name,
                    "enabled_at": time.time()
                }
                
                self._save_secret_info(friend_uid, secret_info)
                return True
                
            except Exception as e:
                logger.error(f"Error enabling secret: {e}")
                return False
            finally:
                driver.quit()
                
        except Exception as e:
            logger.error(f"Secret conversation error: {e}")
            return False
    
    def _save_secret_info(self, friend_uid, secret_info):
        """Save secret conversation info"""
        file_path = os.path.join(self.data_dir, f"{friend_uid}_secret.json")
        with open(file_path, 'w') as f:
            json.dump(secret_info, f, indent=2)
