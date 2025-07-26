"""
Binance API integration module.
Handles price data fetching and trade execution.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import requests
from .config import Config
from .schemas import TradingAnalysis

logger = logging.getLogger(__name__)


class BinanceHandler:
    """Handles all Binance API interactions."""
    
    def __init__(self, config: Config):
        """Initialize Binance handler using public API only."""
        self.config = config
        
        # Use public API only - no authentication needed
        self.client = None
        self.has_api_access = False
        
        # Base URL for public API
        self.base_url = "https://api.binance.com"  # Always use mainnet public API
        
        logger.info("Binance handler initialized with public API access only")
        
    async def fetch_btc_price_history(self, days: int = 15) -> List[Dict[str, Any]]:
        """
        Fetch BTC price history for the specified number of days using public API.
        
        Args:
            days: Number of days to fetch data for
            
        Returns:
            List of price data dictionaries
        """
        try:
            # Calculate start time
            end_time = datetime.now()
            start_time = end_time - timedelta(days=days)
            
            # Use public API endpoint
            url = f"{self.base_url}/api/v3/klines"
            params = {
                "symbol": "BTCUSDT",
                "interval": "1d",
                "startTime": int(start_time.timestamp() * 1000),
                "endTime": int(end_time.timestamp() * 1000),
                "limit": days
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            klines = response.json()
            logger.info("Fetched price history from public API")
            
            # Format the data
            price_data = []
            for kline in klines:
                price_data.append({
                    "timestamp": datetime.fromtimestamp(kline[0] / 1000),
                    "open": float(kline[1]),
                    "high": float(kline[2]),
                    "low": float(kline[3]),
                    "close": float(kline[4]),
                    "volume": float(kline[5])
                })
            
            logger.info(f"Fetched {len(price_data)} days of BTC price data")
            return price_data
            
        except Exception as e:
            logger.error(f"Error fetching price history: {e}")
            raise
    
    async def get_current_btc_price(self) -> float:
        """Get the current BTC price using public API."""
        try:
            # Use public API endpoint
            url = f"{self.base_url}/api/v3/ticker/price"
            params = {"symbol": "BTCUSDT"}
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.info("Fetched BTC price from public API")
            return float(data["price"])
        except Exception as e:
            logger.error(f"Error fetching current price: {e}")
            raise
    
    async def get_account_balance(self) -> Dict[str, float]:
        """Get account balance for BTC and USDT - returns demo data since we're using public API only."""
        logger.info("Using public API - returning demo balance data for testing")
        # Return demo data for testing without API keys
        return {
            "BTC": {"free": 0.001, "locked": 0.0},
            "USDT": {"free": 1000.0, "locked": 0.0}
        }
    
    async def get_usdt_balance(self) -> float:
        """Get current USDT balance (free + locked)."""
        try:
            balances = await self.get_account_balance()
            usdt_data = balances.get("USDT", {"free": 0.0, "locked": 0.0})
            total_usdt = usdt_data["free"] + usdt_data["locked"]
            return total_usdt
        except Exception as e:
            logger.error(f"Error fetching USDT balance: {e}")
            raise
    
    async def get_btc_balance(self) -> float:
        """Get current BTC balance (free + locked)."""
        try:
            balances = await self.get_account_balance()
            btc_data = balances.get("BTC", {"free": 0.0, "locked": 0.0})
            total_btc = btc_data["free"] + btc_data["locked"]
            return total_btc
        except Exception as e:
            logger.error(f"Error fetching BTC balance: {e}")
            raise
    
    async def get_portfolio_value_usdt(self) -> Dict[str, float]:
        """Get total portfolio value in USDT."""
        try:
            # Get current balances
            btc_balance = await self.get_btc_balance()
            usdt_balance = await self.get_usdt_balance()
            
            # Get current BTC price
            btc_price = await self.get_current_btc_price()
            
            # Calculate values
            btc_value_usdt = btc_balance * btc_price
            total_value = btc_value_usdt + usdt_balance
            
            # Calculate allocations
            btc_allocation = (btc_value_usdt / total_value * 100) if total_value > 0 else 0
            usdt_allocation = (usdt_balance / total_value * 100) if total_value > 0 else 0
            
            return {
                "btc_balance": btc_balance,
                "btc_price": btc_price,
                "btc_value_usdt": btc_value_usdt,
                "usdt_balance": usdt_balance,
                "total_value_usdt": total_value,
                "btc_allocation_percent": btc_allocation,
                "usdt_allocation_percent": usdt_allocation
            }
            
        except Exception as e:
            logger.error(f"Error calculating portfolio value: {e}")
            raise
    
    async def get_btc_buying_power(self) -> Dict[str, float]:
        """Calculate how much BTC can be bought with current USDT."""
        try:
            usdt_balance = await self.get_usdt_balance()
            btc_price = await self.get_current_btc_price()
            
            # Calculate buying power (reserve small amount for fees)
            usable_usdt = usdt_balance * 0.999  # Reserve 0.1% for fees
            max_btc_buyable = usable_usdt / btc_price if btc_price > 0 else 0
            
            return {
                "usdt_balance": usdt_balance,
                "btc_price": btc_price,
                "usable_usdt": usable_usdt,
                "max_btc_buyable": max_btc_buyable
            }
            
        except Exception as e:
            logger.error(f"Error calculating buying power: {e}")
            raise
    
    async def execute_trade(self, analysis: TradingAnalysis) -> Dict[str, Any]:
        """
        Execute a trade based on the analysis - simulated since using public API only.
        
        Args:
            analysis: The trading analysis with action and amount
            
        Returns:
            Trade execution result
        """
        logger.info("Using public API - simulating trade execution")
        return {
            "status": "simulated", 
            "message": "Trade simulated (using public API only)",
            "action": analysis.intention,
            "amount": analysis.amount
        }
    
    async def place_buy_order(self, symbol: str, amount: float) -> Dict[str, Any]:
        """
        Place a buy order - simulated since using public API only.
        
        Args:
            symbol: Trading pair symbol (e.g., "BTCUSDT")
            amount: Amount to buy
            
        Returns:
            Order execution result
        """
        logger.info("Using public API - simulating buy order")
        return {
            "status": "simulated", 
            "message": f"Buy order simulated: {amount} {symbol}",
            "symbol": symbol,
            "side": "BUY",
            "quantity": amount
        }
    
    async def place_sell_order(self, symbol: str, amount: float) -> Dict[str, Any]:
        """
        Place a sell order - simulated since using public API only.
        
        Args:
            symbol: Trading pair symbol (e.g., "BTCUSDT")
            amount: Amount to sell
            
        Returns:
            Order execution result
        """
        logger.info("Using public API - simulating sell order")
        return {
            "status": "simulated", 
            "message": f"Sell order simulated: {amount} {symbol}",
            "symbol": symbol,
            "side": "SELL",
            "quantity": amount
        }
    
    def format_price_data_for_llm(self, price_data: List[Dict[str, Any]]) -> str:
        """
        Format price data for LLM consumption.
        
        Args:
            price_data: List of price data dictionaries
            
        Returns:
            Formatted string for LLM analysis
        """
        if not price_data:
            return "No price data available"
        
        formatted = "BTC Price History (Last 15 days):\n"
        formatted += "Date | Open | High | Low | Close | Volume\n"
        formatted += "-" * 50 + "\n"
        
        for data in price_data[-15:]:  # Last 15 days
            formatted += (
                f"{data['timestamp'].strftime('%Y-%m-%d')} | "
                f"${data['open']:.2f} | "
                f"${data['high']:.2f} | "
                f"${data['low']:.2f} | "
                f"${data['close']:.2f} | "
                f"{data['volume']:.2f}\n"
            )
        
        # Add basic statistics
        closes = [d['close'] for d in price_data]
        if len(closes) > 1:
            price_change = closes[-1] - closes[0]
            price_change_pct = (price_change / closes[0]) * 100
            formatted += f"\nPeriod Change: ${price_change:.2f} ({price_change_pct:.2f}%)\n"
            formatted += f"Highest: ${max(d['high'] for d in price_data):.2f}\n"
            formatted += f"Lowest: ${min(d['low'] for d in price_data):.2f}\n"
        
        return formatted


async def main():
    """
    Test all Binance handler endpoints to verify they work with public API.
    """
    print("🚀 Testing Binance Handler with Public API")
    print("=" * 60)
    
    try:
        # Import config here to avoid circular imports
        from .config import load_config
        
        # Initialize handler
        config = load_config()
        handler = BinanceHandler(config)
        
        print(f"📡 API Access: {handler.has_api_access}")
        print(f"🌐 Base URL: {handler.base_url}")
        print()
        
        # Test 1: Current BTC Price
        print("1️⃣ Testing get_current_btc_price()...")
        try:
            price = await handler.get_current_btc_price()
            print(f"   ✅ Current BTC Price: ${price:,.2f}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 2: Price History
        print("2️⃣ Testing fetch_btc_price_history()...")
        try:
            history = await handler.fetch_btc_price_history(7)  # Last 7 days
            print(f"   ✅ Fetched {len(history)} days of price data")
            if history:
                latest = history[-1]
                print(f"   📅 Latest: {latest['timestamp'].strftime('%Y-%m-%d')} - Close: ${latest['close']:.2f}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 3: Account Balance (Demo)
        print("3️⃣ Testing get_account_balance()...")
        try:
            balance = await handler.get_account_balance()
            print(f"   ✅ Demo Balance:")
            for asset, data in balance.items():
                total = data['free'] + data['locked']
                print(f"      {asset}: {total:.6f} (Free: {data['free']:.6f}, Locked: {data['locked']:.6f})")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 4: USDT Balance
        print("4️⃣ Testing get_usdt_balance()...")
        try:
            usdt = await handler.get_usdt_balance()
            print(f"   ✅ USDT Balance: {usdt:.2f} USDT")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 5: BTC Balance
        print("5️⃣ Testing get_btc_balance()...")
        try:
            btc = await handler.get_btc_balance()
            print(f"   ✅ BTC Balance: {btc:.6f} BTC")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 6: Portfolio Value
        print("6️⃣ Testing get_portfolio_value_usdt()...")
        try:
            portfolio = await handler.get_portfolio_value_usdt()
            print(f"   ✅ Portfolio Summary:")
            print(f"      BTC Holdings: {portfolio['btc_balance']:.6f} BTC")
            print(f"      BTC Price: ${portfolio['btc_price']:,.2f}")
            print(f"      BTC Value: ${portfolio['btc_value_usdt']:,.2f} USDT")
            print(f"      USDT Balance: ${portfolio['usdt_balance']:,.2f} USDT")
            print(f"      Total Value: ${portfolio['total_value_usdt']:,.2f} USDT")
            print(f"      BTC Allocation: {portfolio['btc_allocation_percent']:.1f}%")
            print(f"      USDT Allocation: {portfolio['usdt_allocation_percent']:.1f}%")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 7: Buying Power
        print("7️⃣ Testing get_btc_buying_power()...")
        try:
            buying_power = await handler.get_btc_buying_power()
            print(f"   ✅ Buying Power Analysis:")
            print(f"      USDT Balance: {buying_power['usdt_balance']:.2f} USDT")
            print(f"      BTC Price: ${buying_power['btc_price']:,.2f}")
            print(f"      Usable USDT (after fees): {buying_power['usable_usdt']:.2f} USDT")
            print(f"      Max BTC Buyable: {buying_power['max_btc_buyable']:.6f} BTC")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 8: Trade Simulation
        print("8️⃣ Testing execute_trade() (simulated)...")
        try:
            from .schemas import TradingAnalysis
            
            # Create a mock trading analysis
            mock_analysis = TradingAnalysis(
                intention="buy",
                analysis="Test market analysis for simulation",
                suggested_action="Buy 0.001 BTC for testing",
                amount=0.001,
                confidence=0.8,
                risk_level="medium"
            )
            
            result = await handler.execute_trade(mock_analysis)
            print(f"   ✅ Trade Simulation Result:")
            print(f"      Status: {result['status']}")
            print(f"      Message: {result['message']}")
            print(f"      Action: {result['action']}")
            print(f"      Amount: {result['amount']} BTC")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 9: Buy Order Simulation
        print("9️⃣ Testing place_buy_order() (simulated)...")
        try:
            buy_result = await handler.place_buy_order("BTCUSDT", 0.001)
            print(f"   ✅ Buy Order Simulation:")
            print(f"      Status: {buy_result['status']}")
            print(f"      Message: {buy_result['message']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 10: Sell Order Simulation
        print("🔟 Testing place_sell_order() (simulated)...")
        try:
            sell_result = await handler.place_sell_order("BTCUSDT", 0.001)
            print(f"   ✅ Sell Order Simulation:")
            print(f"      Status: {sell_result['status']}")
            print(f"      Message: {sell_result['message']}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        # Test 11: Format Price Data for LLM
        print("1️⃣1️⃣ Testing format_price_data_for_llm()...")
        try:
            history = await handler.fetch_btc_price_history(5)  # Last 5 days
            formatted = handler.format_price_data_for_llm(history)
            print(f"   ✅ Formatted price data for LLM:")
            print("   " + "\n   ".join(formatted.split("\n")[:10]))  # Show first 10 lines
            print("   ... (truncated)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        print()
        
        print("🎉 All endpoint tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Fatal error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
