#!/usr/bin/env python3
"""
WhatsApp Bot Setup Script
Installs Node.js dependencies for WhatsApp integration.
"""

import os
import subprocess
import sys

def check_node_js():
    """Check if Node.js is installed."""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False

def check_npm():
    """Check if npm is installed."""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm found: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False

def install_whatsapp_dependencies():
    """Install WhatsApp bridge dependencies."""
    bridge_dir = os.path.join(os.path.dirname(__file__), 'whatsapp_bridge')
    
    if not os.path.exists(bridge_dir):
        print("❌ WhatsApp bridge directory not found")
        return False
    
    try:
        print("📦 Installing WhatsApp bridge dependencies...")
        os.chdir(bridge_dir)
        
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ WhatsApp dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 WhatsApp Bot Setup")
    print("=" * 25)
    
    # Check prerequisites
    print("\n🔍 Checking prerequisites...")
    
    if not check_node_js():
        print("\n❌ Node.js is required for WhatsApp integration")
        print("📥 Install Node.js from: https://nodejs.org/")
        print("   Recommended: Download and install the LTS version")
        return False
    
    if not check_npm():
        print("\n❌ npm is required (usually comes with Node.js)")
        return False
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_whatsapp_dependencies():
        return False
    
    print("\n" + "=" * 25)
    print("✅ WhatsApp bot setup complete!")
    print("\n🎯 Next steps:")
    print("1. Make sure WhatsApp Web is NOT open in your browser")
    print("2. Run: python3 run_whatsapp_bot.py")
    print("3. Scan the QR code with your phone")
    print("4. Start chatting with your bot!")
    print("\n⚠️  Important: Keep your phone connected to the internet")

if __name__ == "__main__":
    main()
