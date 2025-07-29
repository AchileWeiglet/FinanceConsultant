# Tests Directory

This directory contains all test files for the AI Trading Bot project.

## Test Files

### Core Functionality Tests
- `test_setup.py` - Basic setup and configuration tests
- `test_telegram.py` - Telegram bot functionality tests

### News Sentiment Tests
- `test_btc_news.py` - Tests BTC news intent classification
- `test_news_sentiment.py` - Tests news sentiment analysis feature
- `test_direct_news_sentiment.py` - Direct news sentiment handler tests
- `test_explicit_news.py` - Explicit news sentiment requests
- `test_premium_news.py` - Premium AI news sentiment tests

### AI Integration Tests
- `test_intent_classification.py` - Intent classification accuracy tests
- `test_premium_ai.py` - Premium AI comparison tests
- `test_raw_llm.py` - Raw LLM response tests

## Running Tests

From the project root directory:

```bash
# Run a specific test
python3 tests/test_news_sentiment.py

# Run all news-related tests
python3 tests/test_btc_news.py
python3 tests/test_news_sentiment.py
python3 tests/test_premium_news.py

# Run setup tests
python3 tests/test_setup.py
```

## Test Organization

- **Unit Tests**: Test individual functions and components
- **Integration Tests**: Test interactions between components
- **Feature Tests**: Test complete features end-to-end
- **AI Tests**: Test AI model responses and accuracy

## Adding New Tests

When adding new tests:
1. Follow the naming convention: `test_<feature_name>.py`
2. Include proper error handling and logging
3. Use descriptive test names and documentation
4. Test both success and failure scenarios
