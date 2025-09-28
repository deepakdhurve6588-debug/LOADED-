import json
import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

logger = logging.getLogger(__name__)

class AppStateManager:
    def __init__(self, appstate_file="data/appstate.json"):
        self.appstate_file = appstate_file
        os.makedirs(os.path.dirname(appstate_file), exist_ok=True)
    
    def save_appstate(self, appstate):
        """Save appstate to file"""
        try:
            with open(self.appstate_file, 'w') as f:
                json.dump(appstate, f, indent=2)
            logger.info(f"AppState saved to {self.appstate_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving appstate: {e}")
            return False
    
    def load_appstate(self):
        """Load appstate from file"""
        try:
            if os.path.exists(self.appstate_file):
                with open(self.appstate_file, 'r') as f:
                    appstate = json.load(f)
                logger.info(f"AppState loaded from {self.appstate_file}")
                return appstate
            return []
        except Exception as e:
            logger.error(f"Error loading appstate: {e}")
            return []
    
    def get_appstate_via_selenium(self, email, password):
        """Get appstate using Selenium"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-notifications')
            
            driver = webdriver.Chrome(options=options)
            driver.get("https://facebook.com")
            time.sleep(2)
            
            # Login
            email_field = driver.find_element(By.ID, "email")
            password_field = driver.find_element(By.ID, "pass")
            
            email_field.send_keys(email)
            password_field.send_keys(password)
            password_field.submit()
            time.sleep(5)
            
            # Get cookies
            cookies = driver.get_cookies()
            appstate = []
            
            for cookie in cookies:
                appstate.append({
                    'name': cookie['name'],
                    'value': cookie['value'],
                    'domain': cookie.get('domain', '.facebook.com'),
                    'path': cookie.get('path', '/')
                })
            
            driver.quit()
            return appstate
            
        except Exception as e:
            logger.error(f"Error getting appstate: {e}")
            return []
