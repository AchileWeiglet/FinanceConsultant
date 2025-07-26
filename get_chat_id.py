#!/usr/bin/env python3
"""
Helper script to get your Telegram chat ID.
Run this script after setting your bot token, then send a message to your bot.
"""

import asyncio
import sys
import aiohttp

#!/usr/bin/env python3
"""
Helper script to get your Telegram chat ID.
Run this script after setting your bot token, then send a message to your bot.
"""

import sys
import requests

def get_chat_id(bot_token: str):
    """Get updates from the bot to find your chat ID using direct HTTP API."""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"❌ Error: Bot token might be invalid. Status: {response.status_code}")
            return None
        
        data = response.json()
        
        if not data.get('ok'):
            print(f"❌ Error: {data.get('description', 'Unknown error')}")
            return None
        
        updates = data.get('result', [])
        
        if not updates:
            print("No messages found. Please send a message to your bot first!")
            print(f"Send a message to @finance_helper_norman_bot and run this script again.")
            return None
        
        # Show all chat IDs found
        print("Found chat IDs:")
        chat_ids = set()
        for update in updates:
            if 'message' in update:
                message = update['message']
                chat_id = message['chat']['id']
                user = message.get('from', {})
                username = user.get('username', 'No username')
                first_name = user.get('first_name', 'No name')
                chat_ids.add(chat_id)
                print(f"  Chat ID: {chat_id} (User: {first_name}, @{username})")
        
        if len(chat_ids) == 1:
            chat_id = list(chat_ids)[0]
            print(f"\n✅ Your chat ID is: {chat_id}")
            return chat_id
        else:
            print(f"\n⚠️  Multiple chat IDs found. Use the one that corresponds to your account.")
            return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 get_chat_id.py <bot_token>")
        print("Example: python3 get_chat_id.py 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    get_chat_id(bot_token)
