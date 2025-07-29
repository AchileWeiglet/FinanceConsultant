#!/bin/bash
# Quick Bot Restart Script
# Fast restart of Telegram bot only

# Change to parent directory where the bot files are located
cd "$(dirname "$0")/.."

echo "🚀 Quick Telegram Bot Restart"
echo "=============================="

# Kill existing Telegram bot
echo "🔄 Stopping Telegram bot..."
pkill -f "run_telegram_bot.py" 2>/dev/null
sleep 1

# Force kill if still running
pkill -9 -f "run_telegram_bot.py" 2>/dev/null
sleep 1

# Start Telegram bot
echo "🚀 Starting Telegram bot..."
python3 scripts/run_telegram_bot.py &
TELEGRAM_PID=$!

# Check if started successfully
sleep 2
if ps -p $TELEGRAM_PID > /dev/null; then
    echo "✅ Telegram bot restarted successfully (PID: $TELEGRAM_PID)"
    echo "📋 Log file: tail -f trading_bot.log"
else
    echo "❌ Failed to start Telegram bot"
    exit 1
fi
