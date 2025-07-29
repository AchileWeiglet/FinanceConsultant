#!/bin/bash
# Bot Refresh Script
# Kills existing bot processes and restarts the Telegram bot

echo "🔄 Refreshing Trading Bot..."
echo "========================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Kill existing bot processes
print_status "Killing existing bot processes..."

# Kill Python processes running bot files
pkill -f "run_telegram_bot.py" 2>/dev/null
pkill -f "run_whatsapp_bot.py" 2>/dev/null
pkill -f "run_console_bot.py" 2>/dev/null
pkill -f "telegram_bot.py" 2>/dev/null
pkill -f "whatsapp_bot.py" 2>/dev/null
pkill -f "console_bot.py" 2>/dev/null

# Wait a moment for processes to terminate
sleep 2

# Check if any bot processes are still running
REMAINING_PROCESSES=$(pgrep -f "run_.*_bot.py" 2>/dev/null)
if [ -n "$REMAINING_PROCESSES" ]; then
    print_warning "Some processes still running, force killing..."
    pkill -9 -f "run_.*_bot.py" 2>/dev/null
    sleep 1
fi

print_success "All bot processes terminated"

# Step 2: Check if Ollama is running
print_status "Checking Ollama status..."
if pgrep -x "ollama" > /dev/null; then
    print_success "Ollama is running"
else
    print_warning "Ollama is not running. Starting Ollama..."
    ollama serve &
    sleep 3
    if pgrep -x "ollama" > /dev/null; then
        print_success "Ollama started successfully"
    else
        print_error "Failed to start Ollama. Please start it manually: ollama serve"
    fi
fi

# Step 3: Validate environment
print_status "Validating environment..."

if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    print_error "requirements.txt not found!"
    exit 1
fi

print_success "Environment files found"

# Step 4: Install/update dependencies (optional)
read -p "Update Python dependencies? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Updating Python dependencies..."
    python3 -m pip install -r requirements.txt
    print_success "Dependencies updated"
fi

# Step 5: Choose which bot to start
echo ""
print_status "Which bot would you like to start?"
echo "1) Telegram Bot (Default)"
echo "2) WhatsApp Bot"
echo "3) Console Bot"
echo "4) All Bots"
echo ""
read -p "Enter choice (1-4) [1]: " -n 1 -r
echo

case $REPLY in
    2)
        BOT_CHOICE="whatsapp"
        ;;
    3)
        BOT_CHOICE="console"
        ;;
    4)
        BOT_CHOICE="all"
        ;;
    *)
        BOT_CHOICE="telegram"
        ;;
esac

# Step 6: Start the selected bot(s)
print_status "Starting bot(s)..."

start_telegram_bot() {
    print_status "Starting Telegram bot..."
    python3 run_telegram_bot.py &
    TELEGRAM_PID=$!
    sleep 2
    if ps -p $TELEGRAM_PID > /dev/null; then
        print_success "Telegram bot started successfully (PID: $TELEGRAM_PID)"
    else
        print_error "Failed to start Telegram bot"
    fi
}

start_whatsapp_bot() {
    print_status "Starting WhatsApp bot..."
    python3 run_whatsapp_bot.py &
    WHATSAPP_PID=$!
    sleep 2
    if ps -p $WHATSAPP_PID > /dev/null; then
        print_success "WhatsApp bot started successfully (PID: $WHATSAPP_PID)"
    else
        print_error "Failed to start WhatsApp bot"
    fi
}

start_console_bot() {
    print_status "Starting Console bot..."
    python3 run_console_bot.py
    # Console bot runs in foreground, so no background check needed
}

case $BOT_CHOICE in
    "telegram")
        start_telegram_bot
        ;;
    "whatsapp")
        start_whatsapp_bot
        ;;
    "console")
        start_console_bot
        ;;
    "all")
        start_telegram_bot
        start_whatsapp_bot
        print_warning "Console bot not started in 'all' mode (it requires foreground)"
        ;;
esac

# Step 7: Show running processes
echo ""
print_status "Current bot processes:"
pgrep -f "run_.*_bot.py" -l 2>/dev/null || echo "No bot processes found"

# Step 8: Show logs (for background bots)
if [ "$BOT_CHOICE" != "console" ]; then
    echo ""
    print_status "Bot refresh completed!"
    echo ""
    echo "📋 Useful commands:"
    echo "  • Check logs: tail -f trading_bot.log"
    echo "  • Check WhatsApp logs: tail -f whatsapp_trading_bot.log"
    echo "  • Stop bots: pkill -f 'run_.*_bot.py'"
    echo "  • Monitor processes: ps aux | grep bot"
    echo ""
    echo "💡 The bot is now running in the background."
    echo "   Use 'tail -f trading_bot.log' to see live logs."
fi
