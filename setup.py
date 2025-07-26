#!/usr/bin/env python3
"""
Setup helper script for the trading bot.
Helps users configure their environment and validate setup.
"""

import os
import shutil

def create_env_file():
    """Create .env file from example if it doesn't exist."""
    print("🔧 Setting up environment file...")
    
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env file with your actual API keys!")
        print()
        print("Required configuration:")
        print("1. Get Telegram bot token from @BotFather")
        print("2. Get your Telegram chat ID")
        print("3. Get Binance API keys (use testnet for development)")
        print("4. Make sure Ollama is installed and running")
    else:
        print("❌ .env.example file not found")

def check_ollama():
    """Check if Ollama is accessible."""
    print("\n🤖 Checking Ollama installation...")
    
    # Try to run ollama list command
    import subprocess
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            print("✅ Ollama is installed and accessible")
            
            # Check if llama3 is available
            if 'llama3' in result.stdout:
                print("✅ llama3 model is available")
            else:
                print("⚠️  llama3 model not found")
                print("   Run: ollama pull llama3")
        else:
            print("❌ Ollama command failed")
            print("   Make sure Ollama is installed and running")
    except subprocess.TimeoutExpired:
        print("⚠️  Ollama command timed out")
        print("   Ollama might be starting up, try again in a moment")
    except FileNotFoundError:
        print("❌ Ollama not found")
        print("   Install Ollama from: https://ollama.ai")

def check_dependencies():
    """Check if all required Python packages are installed."""
    print("\n📦 Checking Python dependencies...")
    
    required_packages = [
        'telegram',
        'binance', 
        'requests',
        'aiohttp',
        'pydantic',
        'dotenv',  # This is how python-dotenv is imported
        'openai',
        'google.generativeai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
    else:
        print("\n✅ All required packages are installed")

def main():
    """Main setup function."""
    print("🚀 Trading Bot Setup Helper")
    print("=" * 40)
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Run setup steps
    create_env_file()
    check_dependencies()
    check_ollama()
    
    print("\n" + "=" * 40)
    print("🎯 Setup Summary:")
    print()
    print("Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Test setup: python test_setup.py")
    print("3. Run the bot: python run_bot.py")
    print()
    print("For detailed instructions, see README.md")

if __name__ == "__main__":
    main()
