# Conversational Trading Bot

A proof-of-concept conversational trading bot that integrates **Telegram**, **Ollama LLM**, and **Binance API** for intelligent cryptoc## 🚀 Running the Bot

### Management Scripts

```bash
# Check bot status
./scripts/bot_status.sh

# Quick restart Telegram bot
./scripts/quick_restart.sh

# Full refresh (all bots)
./scripts/refresh_bot.sh
```

### Direct Bot Execution

```bash
# Start Telegram bot
python3 scripts/run_telegram_bot.py

# Start WhatsApp bot
python3 scripts/run_whatsapp_bot.py

# Start console bot
python3 scripts/run_console_bot.py
```rading with human-in-the-loop confirmation.

## 🚀 Features

- **Natural Language Interface**: Chat with your bot using plain English via Telegram
- **Multi-AI Support**: Choose between Ollama (local), OpenAI, or Google Gemini for analysis
- **Human Confirmation**: Never executes trades without explicit user approval
- **Real-time Data**: Fetches live BTC price data and historical trends from Binance
- **Security-First**: Secure API key management and testnet support
- **Modular Architecture**: Clean separation of concerns for easy maintenance

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │◄──►│  Python App     │◄──►│   Binance API   │
│   (User Interface)│   │  (Orchestrator) │   │  (Price & Trade)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Ollama LLM    │
                       │  (AI Analysis)  │
                       └─────────────────┘
```

## 📋 Prerequisites

1. **Python 3.8+**
2. **AI Provider** (choose one):
   - **Ollama** (local) with available models: `llama3.2-vision:11b`, `qwen2.5vl:7b`, `qwen2.5vl:72b`, `gemma3:27b`
   - **OpenAI API** account with API key
   - **Google Gemini API** account with API key
3. **Telegram Bot Token** (from @BotFather)
4. **Binance API Keys** (testnet recommended for development)

## 🛠️ Setup

### 1. Clone and Install Dependencies

```bash
# Navigate to your project directory
cd /path/to/your/project

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
nano .env
```

Required environment variables:
```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Binance Configuration (Use testnet for development!)
BINANCE_API_KEY=your_binance_api_key_here
BINANCE_SECRET_KEY=your_binance_secret_key_here
BINANCE_TESTNET=true

# AI Provider Configuration
AI_PROVIDER=ollama  # Choose: "ollama", "openai", or "gemini"

# Ollama Configuration (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2-vision:11b

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Gemini Configuration (if using Gemini)  
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-pro

# Trading Configuration
ENABLE_TRADING=false  # Set to true to enable actual trading
```

### 3. Set Up AI Provider

Choose one of the following AI providers:

#### Option A: Ollama (Local, Free)
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull one of the available models
ollama pull llama3.2-vision:11b  # Recommended
# Or choose another: qwen2.5vl:7b, qwen2.5vl:72b, gemma3:27b

# Start Ollama service
ollama serve
```

#### Option B: OpenAI (Cloud, Paid)
1. Sign up at [OpenAI](https://platform.openai.com/)
2. Create an API key
3. Add to your `.env`: `OPENAI_API_KEY=your_key_here`
4. Set `AI_PROVIDER=openai`

#### Option C: Google Gemini (Cloud, Paid)
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to your `.env`: `GEMINI_API_KEY=your_key_here`  
3. Set `AI_PROVIDER=gemini`

### 4. Create Telegram Bot

1. Message @BotFather on Telegram
2. Create a new bot with `/newbot`
3. Save the bot token to your `.env` file
4. Get your chat ID by messaging your bot and visiting: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`

### 5. Set Up Binance API

1. Go to [Binance Testnet](https://testnet.binance.vision/) for development
2. Create API keys
3. Add keys to your `.env` file
4. **Important**: Keep `BINANCE_TESTNET=true` for development!

## � Project Structure

```
├── src/                    # Source code
│   ├── ai_factory.py      # AI provider factory
│   ├── binance_handler.py # Binance API integration
│   ├── config.py          # Configuration management
│   ├── functionSelector.py # Intent routing and handling
│   ├── gemini_handler.py  # Google Gemini integration
│   ├── ollama_handler.py  # Ollama LLM integration
│   ├── openai_handler.py  # OpenAI API integration
│   ├── prompts.py         # AI prompts and templates
│   ├── schemas.py         # Data validation schemas
│   ├── telegram_bot.py    # Telegram bot implementation
│   └── whatsapp_bot.py    # WhatsApp bot implementation
├── scripts/               # Management and run scripts
│   ├── bot_status.sh      # Check bot status
│   ├── quick_restart.sh   # Quick Telegram bot restart
│   ├── refresh_bot.sh     # Full bot refresh
│   ├── run_telegram_bot.py # Start Telegram bot
│   ├── run_whatsapp_bot.py # Start WhatsApp bot
│   └── run_console_bot.py  # Start console bot
├── tests/                 # Test files
│   ├── test_setup.py      # Setup tests
│   ├── test_telegram.py   # Telegram functionality tests
│   ├── test_news_sentiment.py # News sentiment tests
│   └── test_*.py          # Various feature tests
├── whatsapp_bridge/       # WhatsApp integration
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## �🚀 Running the Bot

```bash
# Make the run script executable
chmod +x run_bot.py

# Start the bot
python run_bot.py
```

## 💬 Usage Examples

Once your bot is running, you can interact with it via Telegram:

**Commands:**
- `/start` - Get welcome message and help
- `/balance` - Check your account balance
- `/price` - Get current BTC price
- `/status` - Check system status
- `/ai` - Check AI provider status and switch providers

**Natural Language:**
- "How's BTC looking today?"
- "Should I buy some Bitcoin?"
- "Is BTC dropping too fast?"
- "What's the trend for Bitcoin this week?"

**Example Conversation:**
```
You: "Hey, is BTC dropping too fast today?"

Bot: 🤖 Analysis:
Bitcoin has experienced a 5.2% decline over the past 24 hours, breaking below the $42,000 support level. Volume is elevated, suggesting genuine selling pressure rather than low-liquidity moves.

💡 Suggestion: Consider a small buy position if you believe in long-term recovery, as we're approaching the next support zone around $40,000.

🎯 Confidence: 65%
⚠️ Risk Level: MEDIUM

🔄 Proposed Action: BUY 0.001 BTC
Would you like me to execute this trade?

[✅ Yes, Execute] [❌ No, Cancel]
```

## 📁 Project Structure

```
src/
├── __init__.py              # Package initialization
├── main.py                  # Application entry point
├── config.py                # Configuration management
├── schemas.py               # Data models and validation
├── ai_factory.py            # AI provider factory
├── binance_handler.py       # Binance API integration
├── ollama_handler.py        # Ollama LLM communication
├── openai_handler.py        # OpenAI API communication
├── gemini_handler.py        # Google Gemini API communication
└── telegram_bot.py          # Telegram bot interface

.env.example                 # Environment variables template
.env                        # Your actual environment variables (not in git)
requirements.txt            # Python dependencies
run_bot.py                  # Simple runner script
README.md                   # This file
```

## 🔒 Security Notes

- **Never commit `.env` files**: Your API keys should remain private
- **Use testnet first**: Always test with Binance testnet before live trading
- **Enable trading cautiously**: Keep `ENABLE_TRADING=false` until you're confident
- **Monitor logs**: Check `trading_bot.log` for any issues
- **Authorized users only**: Bot checks Telegram chat ID for authorization

## 🐛 Troubleshooting

### Bot doesn't respond
- Check if Ollama is running: `ollama list`
- Verify your Telegram bot token
- Check the logs in `trading_bot.log`

### API errors
- Verify your Binance API keys
- Ensure you're using testnet for development
- Check your internet connection

### Ollama issues
- Restart Ollama: `ollama serve`
- Verify the model is available: `ollama list`
- Check if the service is accessible: `curl http://localhost:11434/api/tags`

## 🤝 Contributing

This is a proof-of-concept project. Feel free to:
- Add new features
- Improve error handling
- Enhance the AI prompts
- Add support for other cryptocurrencies

## ⚠️ Disclaimer

This bot is for educational and research purposes only. Cryptocurrency trading involves significant risk, and you should never invest more than you can afford to lose. The authors are not responsible for any financial losses incurred through the use of this software.

## 📄 License

This project is open source. Use at your own risk and responsibility.
