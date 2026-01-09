"""
Test Stock Scanner - Demonstration Script
This shows the expected output format when the full system is running
"""

def demo_output():
    """
    Demonstration of what the stock scanner returns

    Note: To run the actual scanner, you need to:
    1. Install all dependencies: pip install -r requirements.txt
    2. Run: python app.py
    3. Visit: http://localhost:5000 and click "Scan Now"
    """

    print("=" * 80)
    print("STOCK RECOMMENDATION TOOL - DEMO OUTPUT")
    print("=" * 80)
    print()

    print("📊 TRENDING SECTORS TODAY:")
    print("-" * 80)
    sectors = [
        {"name": "Technology", "performance_day": "+2.45%", "performance_week": "+5.20%"},
        {"name": "Healthcare", "performance_day": "+1.82%", "performance_week": "+3.15%"},
        {"name": "Financial", "performance_day": "+1.45%", "performance_week": "+2.80%"},
        {"name": "Consumer Cyclical", "performance_day": "+1.20%", "performance_week": "+2.50%"},
        {"name": "Industrials", "performance_day": "+0.95%", "performance_week": "+1.90%"},
    ]

    for i, sector in enumerate(sectors, 1):
        print(f"{i}. {sector['name']:20} | Day: {sector['performance_day']:8} | Week: {sector['performance_week']}")

    print()
    print("🚀 BULLISH BREAKOUT STOCKS:")
    print("-" * 80)
    print(f"{'Ticker':<8} {'Price':<10} {'Buy Zone':<20} {'Stop Loss':<12} {'Volume':<12} {'RSI':<8}")
    print("-" * 80)

    breakouts = [
        {"ticker": "NVDA", "price": 142.50, "buy_low": 139.65, "buy_high": 145.35, "stop": 131.10, "vol_ratio": 2.3, "rsi": 65.2},
        {"ticker": "PLTR", "price": 78.25, "buy_low": 76.69, "buy_high": 79.82, "stop": 71.99, "vol_ratio": 2.1, "rsi": 62.8},
        {"ticker": "COIN", "price": 285.60, "buy_low": 279.89, "buy_high": 291.31, "stop": 262.75, "vol_ratio": 1.9, "rsi": 58.4},
    ]

    for stock in breakouts:
        print(f"{stock['ticker']:<8} ${stock['price']:<9.2f} ${stock['buy_low']:.2f} - ${stock['buy_high']:.2f}    ${stock['stop']:<11.2f} {stock['vol_ratio']:.1f}x avg    {stock['rsi']:.1f}")

    print()
    print("🔄 BULLISH REVERSAL STOCKS:")
    print("-" * 80)
    print(f"{'Ticker':<8} {'Price':<10} {'Buy Zone':<20} {'Stop Loss':<12} {'Volume':<12} {'RSI':<8}")
    print("-" * 80)

    reversals = [
        {"ticker": "AMD", "price": 127.85, "buy_low": 125.30, "buy_high": 130.41, "stop": 117.63, "vol_ratio": 1.8, "rsi": 42.5},
        {"ticker": "SQ", "price": 92.40, "buy_low": 90.55, "buy_high": 94.25, "stop": 85.01, "vol_ratio": 1.7, "rsi": 38.9},
        {"ticker": "CRWD", "price": 365.20, "buy_low": 357.90, "buy_high": 372.50, "stop": 336.38, "vol_ratio": 1.6, "rsi": 45.3},
    ]

    for stock in reversals:
        print(f"{stock['ticker']:<8} ${stock['price']:<9.2f} ${stock['buy_low']:.2f} - ${stock['buy_high']:.2f}    ${stock['stop']:<11.2f} {stock['vol_ratio']:.1f}x avg    {stock['rsi']:.1f}")

    print()
    print("📈 HIGH VOLUME BREAKOUT STOCKS:")
    print("-" * 80)
    print(f"{'Ticker':<8} {'Price':<10} {'Buy Zone':<20} {'Stop Loss':<12} {'Volume':<12} {'RSI':<8}")
    print("-" * 80)

    volume_breakouts = [
        {"ticker": "TSLA", "price": 412.75, "buy_low": 404.50, "buy_high": 421.01, "stop": 379.73, "vol_ratio": 3.2, "rsi": 68.7},
        {"ticker": "SMCI", "price": 45.60, "buy_low": 44.69, "buy_high": 46.51, "stop": 41.95, "vol_ratio": 2.8, "rsi": 71.2},
        {"ticker": "MARA", "price": 18.35, "buy_low": 17.98, "buy_high": 18.72, "stop": 16.88, "vol_ratio": 2.5, "rsi": 64.5},
    ]

    for stock in volume_breakouts:
        print(f"{stock['ticker']:<8} ${stock['price']:<9.2f} ${stock['buy_low']:.2f} - ${stock['buy_high']:.2f}    ${stock['stop']:<11.2f} {stock['vol_ratio']:.1f}x avg    {stock['rsi']:.1f}")

    print()
    print("=" * 80)
    print("📋 FILTERING CRITERIA APPLIED:")
    print("=" * 80)
    print("✅ Price > $3.00")
    print("✅ Market Cap > $2 Billion")
    print("✅ Price above 50-day EMA")
    print("✅ Volume > 1.5x average volume")
    print("✅ Bullish technical patterns")
    print()
    print("⚠️  DISCLAIMER: This is example data for demonstration purposes.")
    print("   For live data, install dependencies and run: python app.py")
    print("   Then visit http://localhost:5000 and click 'Scan Now'")
    print()
    print("=" * 80)
    print()
    print("📧 EMAIL REPORT FEATURES:")
    print("   - Automatically sent every day at 7:00 AM")
    print("   - Beautiful HTML formatting with color-coded sectors")
    print("   - Complete stock tables with buy/stop levels")
    print("   - Professional layout for easy reading")
    print()
    print("🔌 API ENDPOINTS AVAILABLE:")
    print("   - GET  /api/recommendations - Get all recommendations")
    print("   - POST /api/scan - Trigger new scan")
    print("   - GET  /api/sectors - Get trending sectors")
    print("   - GET  /api/stock/{ticker} - Analyze specific stock")
    print("   - POST /api/send-email - Send email report")
    print()
    print("=" * 80)


if __name__ == "__main__":
    demo_output()
