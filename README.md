# 📈 Stock Recommendation Tool

AI-Powered stock recommendation system that scans finviz.com for trending sectors and identifies stocks with bullish patterns, breakouts, and reversals. Includes automated daily email reports and on-demand scanning capabilities.

## 🎯 Features

- **Trending Sector Analysis**: Identifies top-performing sectors and industries
- **Bullish Breakout Detection**: Finds stocks breaking out above resistance with high volume
- **Bullish Reversal Identification**: Spots reversal patterns in oversold stocks
- **Technical Analysis**: 50 EMA, RSI, MACD, and volume analysis
- **Smart Filtering**: Only stocks above $3, $2B+ market cap, and above 50 EMA
- **Buy/Stop Loss Calculations**: Automatic risk management levels
- **Daily Email Reports**: Automated reports every morning at 7 AM
- **On-Demand Scanning**: Web interface and API for manual scans
- **Beautiful HTML Reports**: Professional email formatting

## 📋 Stock Filtering Criteria

All recommended stocks must meet these criteria:
- ✅ Price > $3
- ✅ Market Cap > $2 Billion
- ✅ Price above 50-day EMA
- ✅ Volume > 1.5x average (high volume breakout)
- ✅ Bullish chart patterns (breakouts or reversals)
- ✅ Positive technical indicators

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd flask-app

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAILS=recipient1@example.com,recipient2@example.com

# Flask Configuration
SECRET_KEY=your-random-secret-key
DEBUG=True
```

**Gmail Users**: You need to use an [App Password](https://support.google.com/accounts/answer/185833), not your regular Gmail password.

### 3. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## 📱 Web Interface

Access the web interface at `http://localhost:5000` to:
- View system status
- Trigger manual scans
- Send test emails
- View API endpoints

## 🔌 API Endpoints

### Get Recommendations
```bash
GET http://localhost:5000/api/recommendations
```
Returns cached stock recommendations from the last scan.

### Trigger Manual Scan
```bash
POST http://localhost:5000/api/scan
```
Triggers an immediate stock scan and returns results.

### Get Trending Sectors
```bash
GET http://localhost:5000/api/sectors
```
Returns trending sector performance data.

### Get Stock Details
```bash
GET http://localhost:5000/api/stock/AAPL
```
Returns detailed technical analysis for a specific ticker.

### Send Email Report
```bash
POST http://localhost:5000/api/send-email
```
Manually triggers sending the email report.

### System Status
```bash
GET http://localhost:5000/api/status
```
Returns system status and scheduler information.

## 📧 Email Reports

The system automatically sends email reports every day at **7:00 AM** with:
- Top trending sectors
- Bullish breakout stocks
- Bullish reversal opportunities
- High volume breakout stocks
- Buy zones and stop loss levels for each stock

You can also trigger manual email sends via the web interface or API.

## 🛠️ Configuration Options

Edit `config.py` to customize:

```python
# Stock Filtering
MIN_PRICE = 3.0                    # Minimum stock price
MIN_MARKET_CAP = 2_000_000_000     # $2 billion minimum
VOLUME_MULTIPLIER = 1.5            # Volume breakout threshold
EMA_PERIOD = 50                    # EMA period for trend

# Risk Management
STOP_LOSS_PERCENT = 0.08           # 8% stop loss
BUY_ZONE_PERCENT = 0.02            # 2% buy zone range

# Scheduling
REPORT_TIME = "07:00"              # Daily report time
```

## 📁 Project Structure

```
flask-app/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── finviz_scraper.py      # Finviz data scraper
├── technical_analysis.py  # Technical analysis engine
├── stock_recommender.py   # Stock recommendation logic
├── email_reporter.py      # Email report generator
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔍 How It Works

1. **Data Collection**: Scrapes finviz.com for stocks meeting basic criteria
2. **Technical Analysis**: Analyzes each stock using yfinance data for:
   - 50-day EMA position
   - Volume analysis (current vs average)
   - RSI and MACD indicators
   - Pattern detection (breakouts/reversals)
3. **Filtering**: Applies strict criteria to identify high-probability setups
4. **Risk Calculation**: Determines optimal buy zones and stop losses
5. **Reporting**: Generates beautiful HTML reports with all recommendations
6. **Delivery**: Emails reports automatically at 7 AM daily

## 📊 Example Output

Each stock recommendation includes:
- **Ticker Symbol**: Stock identifier
- **Current Price**: Latest closing price
- **Buy Zone**: Suggested entry range
- **Stop Loss**: Risk management level
- **Volume Ratio**: Current volume vs average
- **RSI**: Relative Strength Index
- **Pattern Type**: Breakout, reversal, or volume breakout
- **Recommendation**: AI-generated trading suggestion

## ⚠️ Disclaimer

This tool is for **informational and educational purposes only**. It is NOT financial advice.

- Always conduct your own research
- Consult with a licensed financial advisor
- Never invest more than you can afford to lose
- Past performance does not guarantee future results
- The creators are not responsible for trading losses

## 🐛 Troubleshooting

### Email not sending
- Verify SMTP credentials in `.env`
- For Gmail, use an App Password
- Check firewall/antivirus blocking port 587

### No stocks found
- Market conditions may not have qualifying stocks
- Try adjusting filters in `config.py`
- Check finviz.com is accessible

### Scan taking too long
- Reduce `max_stocks` in `stock_recommender.py`
- Adjust `max_workers` for parallel processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is for educational purposes. Use at your own risk.

## 🙏 Acknowledgments

- Data provided by [Finviz.com](https://finviz.com)
- Technical analysis powered by [yfinance](https://github.com/ranaroussi/yfinance) and [pandas-ta](https://github.com/twopirllc/pandas-ta)
- Built with [Flask](https://flask.palletsprojects.com/) and [APScheduler](https://apscheduler.readthedocs.io/)

---

**Happy Trading! 📈💰**
