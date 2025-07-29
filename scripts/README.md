# Scripts Directory

This directory contains all executable scripts for managing and running the AI Trading Bot.

## Bot Management Scripts

### Shell Scripts (Management)
- `refresh_bot.sh` - Complete bot refresh and restart
- `quick_restart.sh` - Quick Telegram bot restart only
- `bot_status.sh` - Check status of all bot processes

### Python Run Scripts
- `run_telegram_bot.py` - Start Telegram bot
- `run_whatsapp_bot.py` - Start WhatsApp bot
- `run_console_bot.py` - Start console/CLI bot
- `run_bot.py` - General bot runner script

## Usage

### From Project Root Directory:

```bash
# Check bot status
./scripts/bot_status.sh

# Quick restart Telegram bot
./scripts/quick_restart.sh

# Full bot refresh
./scripts/refresh_bot.sh

# Start specific bots
python3 scripts/run_telegram_bot.py
python3 scripts/run_whatsapp_bot.py
python3 scripts/run_console_bot.py
```

### Direct Script Execution:

```bash
# From scripts directory
cd scripts

# Management
./bot_status.sh
./quick_restart.sh
./refresh_bot.sh

# Bot runners (from parent directory)
cd ..
python3 scripts/run_telegram_bot.py
```

## Script Features

### Bot Status (`bot_status.sh`)
- Shows running/stopped status for all bots
- Displays process IDs (PIDs)
- Shows recent log entries
- Checks Ollama service status

### Quick Restart (`quick_restart.sh`)
- Fast Telegram bot restart
- Minimal downtime
- Automatic status verification
- Background process management

### Full Refresh (`refresh_bot.sh`)
- Stops all bot processes
- Cleans up orphaned processes
- Interactive bot selection
- Comprehensive status reporting

## Permissions

Make sure scripts are executable:
```bash
chmod +x scripts/*.sh
```

## Logs

Bot logs are written to the project root:
- `trading_bot.log` - Telegram bot logs
- `whatsapp_trading_bot.log` - WhatsApp bot logs

Monitor logs:
```bash
tail -f trading_bot.log
tail -f whatsapp_trading_bot.log
```
