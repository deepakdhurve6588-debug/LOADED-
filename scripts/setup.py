#!/usr/bin/env python3
"""
Setup script for Deepak Bot
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.utils import create_directories

def main():
    print("🚀 Setting up Deepak Messenger Bot...")
    
    # Create directories
    create_directories()
    
    print("✅ Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your credentials")
    print("2. Run: python scripts/get_appstate.py")
    print("3. Run: python scripts/generate_keys.py")
    print("4. Run: python scripts/enable_secret.py")
    print("5. Run: python app.py")

if __name__ == "__main__":
    main()
