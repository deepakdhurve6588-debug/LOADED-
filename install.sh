#!/data/data/com.termux/files/usr/bin/bash

echo "🤖 LOADED Bot - Termux Installer"
echo "================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_status() { echo -e "${GREEN}[✓]${NC} $1"; }
print_error() { echo -e "${RED}[✗]${NC} $1"; }

# Update packages
print_status "Updating packages..."
pkg update -y && pkg upgrade -y

# Install dependencies
print_status "Installing dependencies..."
pkg install -y python git wget curl

# Install Firefox
print_status "Installing Firefox..."
pkg install -y firefox

# Install GeckoDriver
print_status "Installing GeckoDriver..."
pkg install -y geckodriver

# Install Python packages
print_status "Installing Python packages..."
pip install selenium

# Download bot files
print_status "Downloading bot files..."
cd ~/
wget -q https://raw.githubusercontent.com/deepakdhurve6588-debug/LOADED-/main/loaded-bot.py -O loaded-bot.py

# Make executable
chmod +x loaded-bot.py

print_status "Installation completed!"
echo ""
echo "🚀 Run the bot:"
echo "   python loaded-bot.py"
echo ""
echo "📱 GitHub: https://github.com/deepakdhurve6588-debug/LOADED-"
