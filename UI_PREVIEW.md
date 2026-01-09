# 🎨 Stock Recommendation Tool - UI Preview

## Web Interface Layout

When you access `http://localhost:5000`, here's what you see:

```
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║          📈 Stock Recommendation Tool                              ║
║          AI-Powered Stock Analysis with Finviz Data               ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  Status: System Active 🟢                                         │
│  Last Scan: 2026-01-08 14:30:00                                   │
│  Next Scheduled Report: Tomorrow at 7:00 AM                       │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ 🔍 Scan Now  │  │ 📊 View JSON Data│  │ 📧 Send Test Email│
└──────────────┘  └──────────────────┘  └──────────────────┘
   ⬆ CLICK ME!       ⬆ Opens API         ⬆ Email Preview


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        🎯 Key Features

┌────────────────────┬────────────────────┬────────────────────┐
│ 📊 Technical       │ 🔥 Trending        │ 🚀 Breakout        │
│    Analysis        │    Sectors         │    Detection       │
│                    │                    │                    │
│ 50 EMA, RSI,      │ Identify hot       │ Automatic          │
│ Volume analysis,   │ sectors and        │ detection of       │
│ and pattern        │ industries with    │ bullish breakouts  │
│ detection          │ real-time data     │ with high volume   │
└────────────────────┴────────────────────┴────────────────────┘

┌────────────────────┬────────────────────┬────────────────────┐
│ 🔄 Reversal        │ 💰 Risk            │ 📧 Daily           │
│    Patterns        │    Management      │    Reports         │
│                    │                    │                    │
│ Spot bullish       │ Automated buy      │ Automated email    │
│ reversal           │ zone and stop      │ reports delivered  │
│ opportunities      │ loss calculations  │ at 7 AM daily      │
└────────────────────┴────────────────────┴────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                      🔌 API Endpoints

  GET  /api/recommendations - Get all stock recommendations
  GET  /api/sectors - Get trending sectors
  POST /api/scan - Trigger manual stock scan
  GET  /api/stock/{ticker} - Get details for specific stock

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                   📋 Filtering Criteria

  ✅ Price above $3
  ✅ Market cap over $2 billion
  ✅ Price above 50-day EMA
  ✅ High volume breakout (1.5x average)
  ✅ Bullish chart patterns
  ✅ Strong technical indicators

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

     © 2026 Stock Recommendation Tool | Powered by Finviz
```

## 🎬 Interactive Elements

### 1. **Scan Now Button** - Click to:
   - Trigger immediate stock scan
   - Shows loading spinner with animation
   - Displays alert with results: "Found 15 stocks!"
   - Updates "Last Scan" timestamp automatically

### 2. **View JSON Data** - Click to:
   - Opens `/api/recommendations` endpoint
   - Shows raw JSON data for all recommendations
   - Can be used by other applications/scripts

### 3. **Send Test Email** - Click to:
   - Prompts confirmation dialog
   - Sends email to configured recipients
   - Shows success/failure notification

### 4. **Loading Animation**
   ```
   ⏳ Scanning stocks... This may take a minute.

      ⚫ ← Spinning animation appears
   ```

## 🎨 Visual Design

- **Color Scheme**: Purple gradient (professional trading theme)
- **Typography**: Segoe UI (clean, modern)
- **Layout**: Responsive grid (works on all devices)
- **Animations**: Hover effects, smooth transitions
- **Status Indicators**: Real-time updates with emojis

## 📊 API Response Example

When you click "Scan Now", the system returns:

```json
{
  "trending_sectors": [
    {
      "name": "Technology",
      "performance_day": 2.45,
      "performance_week": "5.20%"
    }
  ],
  "bullish_breakouts": [
    {
      "ticker": "NVDA",
      "current_price": 142.50,
      "buy_price_low": 139.65,
      "buy_price_high": 145.35,
      "stop_loss": 131.10,
      "volume_ratio": 2.3,
      "rsi": 65.2,
      "recommendation": "NVDA showing strong Breakout - High conviction buy"
    }
  ],
  "bullish_reversals": [...],
  "high_volume_breakouts": [...]
}
```

## 📧 Email Report Preview

The HTML email sent daily at 7 AM looks like:

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  📈 Stock Recommendations Report                        │
│  Date: January 8, 2026                                  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🔥 Trending Sectors                                    │
│                                                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │Technology│ │Healthcare│ │Financial │              │
│  │  +2.45%  │ │  +1.82%  │ │  +1.45%  │              │
│  └──────────┘ └──────────┘ └──────────┘              │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🚀 Bullish Breakouts                                   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │Ticker│Price  │Buy Zone      │Stop   │Volume │  │
│  ├────────────────────────────────────────────────┤   │
│  │NVDA  │$142.50│$139.65-145.35│$131.10│2.3x   │  │
│  │PLTR  │$78.25 │$76.69-79.82  │$71.99 │2.1x   │  │
│  └────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 🖱️ User Interaction Flow

```
1. User opens http://localhost:5000
        ↓
2. Sees beautiful dashboard with status
        ↓
3. Clicks "🔍 Scan Now" button
        ↓
4. Loading spinner appears
        ↓
5. System scans finviz.com + analyzes stocks
        ↓
6. Alert shows: "Scan complete! Found 12 stocks"
        ↓
7. User clicks "📊 View JSON Data"
        ↓
8. Sees complete recommendations with buy/stop levels
        ↓
9. User clicks "📧 Send Test Email"
        ↓
10. Beautiful HTML email arrives in inbox
```

## 🎯 Mobile Responsive

The UI automatically adapts to mobile devices:

```
┌─────────────┐
│ 📈 Stock    │
│ Reco Tool   │
├─────────────┤
│ Status: 🟢  │
│ Last: 14:30 │
├─────────────┤
│ Scan Now    │
│ View JSON   │
│ Send Email  │
├─────────────┤
│ Features:   │
│ • Technical │
│ • Sectors   │
│ • Breakouts │
└─────────────┘
```

## 🚀 To See the UI Live:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python app.py

# 3. Open browser
http://localhost:5000

# 4. Click buttons and interact!
```

The UI is fully built and ready to use! 🎉
