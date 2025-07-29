#!/usr/bin/env python3
"""
Simple script to run the trading bot.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import asyncio
from src.main import main

if __name__ == "__main__":
    asyncio.run(main())
