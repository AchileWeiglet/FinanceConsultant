#!/bin/bash
# Bot Status Checker
# Shows the current status of all bot processes

echo "🤖 Trading Bot Status"
echo "===================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check Telegram bot
TELEGRAM_PID=$(pgrep -f "run_telegram_bot.py" 2>/dev/null)
if [ -n "$TELEGRAM_PID" ]; then
    echo -e "📱 Telegram Bot: ${GREEN}RUNNING${NC} (PID: $TELEGRAM_PID)"
else
    echo -e "📱 Telegram Bot: ${RED}STOPPED${NC}"
fi

# Check WhatsApp bot
WHATSAPP_PID=$(pgrep -f "run_whatsapp_bot.py" 2>/dev/null)
if [ -n "$WHATSAPP_PID" ]; then
    echo -e "💬 WhatsApp Bot: ${GREEN}RUNNING${NC} (PID: $WHATSAPP_PID)"
else
    echo -e "💬 WhatsApp Bot: ${RED}STOPPED${NC}"
fi

# Check Console bot
CONSOLE_PID=$(pgrep -f "run_console_bot.py" 2>/dev/null)
if [ -n "$CONSOLE_PID" ]; then
    echo -e "🖥️  Console Bot: ${GREEN}RUNNING${NC} (PID: $CONSOLE_PID)"
else
    echo -e "🖥️  Console Bot: ${RED}STOPPED${NC}"
fi

# Check Ollama
OLLAMA_PID=$(pgrep -x "ollama" 2>/dev/null)
if [ -n "$OLLAMA_PID" ]; then
    echo -e "🦙 Ollama: ${GREEN}RUNNING${NC} (PID: $OLLAMA_PID)"
else
    echo -e "🦙 Ollama: ${RED}STOPPED${NC}"
fi

echo ""
echo "📋 Recent log entries:"
echo "======================"

# Show last few lines from Telegram bot log
if [ -f "trading_bot.log" ]; then
    echo -e "${BLUE}📱 Telegram Bot (last 3 lines):${NC}"
    tail -3 trading_bot.log 2>/dev/null | sed 's/^/  /'
    echo ""
fi

# Show last few lines from WhatsApp bot log
if [ -f "whatsapp_trading_bot.log" ]; then
    echo -e "${BLUE}💬 WhatsApp Bot (last 3 lines):${NC}"
    tail -3 whatsapp_trading_bot.log 2>/dev/null | sed 's/^/  /'
    echo ""
fi

echo "💡 Commands:"
echo "  Start: ./refresh_bot.sh"
echo "  Quick restart: ./quick_restart.sh"
echo "  Logs: tail -f trading_bot.log"
echo "  Stop: pkill -f 'run_.*_bot.py'"
