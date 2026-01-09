"""
Stock Recommendation Flask Application
Main application with routes and scheduler
"""
from flask import Flask, render_template_string, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
import json

from config import Config
from stock_recommender import StockRecommender
from email_reporter import EmailReporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize components
recommender = StockRecommender()
email_reporter = EmailReporter()
scheduler = BackgroundScheduler()

# Store last scan results (in-memory cache)
last_scan_results = None
last_scan_time = None


def scheduled_scan_and_email():
    """
    Scheduled job to scan stocks and send email report
    Runs every day at 7 AM
    """
    logger.info("Starting scheduled stock scan...")

    try:
        # Perform stock scan
        recommendations = recommender.scan_stocks()

        # Send email report
        success = email_reporter.send_stock_report(recommendations)

        if success:
            logger.info("Scheduled email report sent successfully")
        else:
            logger.error("Failed to send scheduled email report")

        # Update cache
        global last_scan_results, last_scan_time
        last_scan_results = recommendations
        last_scan_time = datetime.now()

    except Exception as e:
        logger.error(f"Error in scheduled scan: {e}")


# HTML Template for home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock Recommendation Tool</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        .header h1 {
            font-size: 42px;
            margin-bottom: 10px;
        }
        .header p {
            font-size: 18px;
            opacity: 0.9;
        }
        .content {
            padding: 40px;
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            transition: transform 0.3s;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .feature-card h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 20px;
        }
        .feature-card p {
            color: #666;
            line-height: 1.6;
        }
        .button-group {
            display: flex;
            gap: 15px;
            margin: 30px 0;
            flex-wrap: wrap;
        }
        .btn {
            padding: 15px 30px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s;
            font-weight: bold;
        }
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn-secondary {
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }
        .btn-secondary:hover {
            background: #667eea;
            color: white;
        }
        .status-box {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .api-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
        }
        .api-section h3 {
            color: #333;
            margin-bottom: 15px;
        }
        .api-endpoint {
            background: white;
            padding: 10px 15px;
            margin: 10px 0;
            border-radius: 5px;
            font-family: monospace;
            border-left: 3px solid #667eea;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📈 Stock Recommendation Tool</h1>
            <p>AI-Powered Stock Analysis with Finviz Data</p>
        </div>

        <div class="content">
            <div class="status-box">
                <strong>Status:</strong> System Active 🟢<br>
                <strong>Last Scan:</strong> <span id="last-scan">{{ last_scan_time }}</span><br>
                <strong>Next Scheduled Report:</strong> Tomorrow at 7:00 AM
            </div>

            <div class="button-group">
                <button class="btn btn-primary" onclick="scanNow()">🔍 Scan Now</button>
                <a href="/api/recommendations" class="btn btn-secondary">📊 View JSON Data</a>
                <button class="btn btn-secondary" onclick="sendTestEmail()">📧 Send Test Email</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 10px; color: #666;">Scanning stocks... This may take a minute.</p>
            </div>

            <h2 style="margin-top: 40px; color: #333;">🎯 Key Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>📊 Technical Analysis</h3>
                    <p>50 EMA, RSI, Volume analysis, and pattern detection for accurate signals</p>
                </div>
                <div class="feature-card">
                    <h3>🔥 Trending Sectors</h3>
                    <p>Identify hot sectors and industries with real-time performance data</p>
                </div>
                <div class="feature-card">
                    <h3>🚀 Breakout Detection</h3>
                    <p>Automatic detection of bullish breakouts with high volume confirmation</p>
                </div>
                <div class="feature-card">
                    <h3>🔄 Reversal Patterns</h3>
                    <p>Spot bullish reversal opportunities before they take off</p>
                </div>
                <div class="feature-card">
                    <h3>💰 Risk Management</h3>
                    <p>Automated buy zone and stop loss calculations for every recommendation</p>
                </div>
                <div class="feature-card">
                    <h3>📧 Daily Reports</h3>
                    <p>Automated email reports delivered to your inbox every morning at 7 AM</p>
                </div>
            </div>

            <div class="api-section">
                <h3>🔌 API Endpoints</h3>
                <div class="api-endpoint">
                    <strong>GET</strong> /api/recommendations - Get all stock recommendations
                </div>
                <div class="api-endpoint">
                    <strong>GET</strong> /api/sectors - Get trending sectors
                </div>
                <div class="api-endpoint">
                    <strong>POST</strong> /api/scan - Trigger manual stock scan
                </div>
                <div class="api-endpoint">
                    <strong>GET</strong> /api/stock/{ticker} - Get details for specific stock
                </div>
            </div>

            <h2 style="margin-top: 40px; color: #333;">📋 Filtering Criteria</h2>
            <ul style="line-height: 2; color: #666; margin-left: 20px;">
                <li>✅ Price above $3</li>
                <li>✅ Market cap over $2 billion</li>
                <li>✅ Price above 50-day EMA</li>
                <li>✅ High volume breakout (1.5x average)</li>
                <li>✅ Bullish chart patterns</li>
                <li>✅ Strong technical indicators</li>
            </ul>
        </div>

        <div class="footer">
            <p>© 2026 Stock Recommendation Tool | Powered by Finviz & Technical Analysis</p>
            <p style="font-size: 12px; margin-top: 10px;">
                Disclaimer: For informational purposes only. Not financial advice.
            </p>
        </div>
    </div>

    <script>
        function scanNow() {
            document.getElementById('loading').style.display = 'block';
            fetch('/api/scan', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    alert('Scan completed! Found ' + (
                        data.bullish_breakouts.length +
                        data.bullish_reversals.length +
                        data.high_volume_breakouts.length
                    ) + ' stocks. Check /api/recommendations for details.');
                    document.getElementById('last-scan').textContent = new Date().toLocaleString();
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    alert('Error during scan: ' + error);
                });
        }

        function sendTestEmail() {
            if (confirm('Send test email to configured recipients?')) {
                fetch('/api/send-email', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            alert('Test email sent successfully!');
                        } else {
                            alert('Failed to send email: ' + data.message);
                        }
                    })
                    .catch(error => alert('Error: ' + error));
            }
        }
    </script>
</body>
</html>
"""


@app.route('/')
def home():
    """Home page"""
    last_scan_display = last_scan_time.strftime('%Y-%m-%d %H:%M:%S') if last_scan_time else 'Never'
    return render_template_string(HOME_TEMPLATE, last_scan_time=last_scan_display)


@app.route('/api/recommendations')
def get_recommendations():
    """
    API endpoint to get cached stock recommendations

    Returns:
        JSON with stock recommendations
    """
    if last_scan_results is None:
        return jsonify({
            'message': 'No scan results available. Trigger a scan first.',
            'data': None
        }), 404

    return jsonify({
        'scan_time': last_scan_time.isoformat() if last_scan_time else None,
        'data': last_scan_results
    })


@app.route('/api/scan', methods=['POST'])
def trigger_scan():
    """
    API endpoint to trigger manual stock scan

    Returns:
        JSON with scan results
    """
    logger.info("Manual scan triggered via API")

    try:
        recommendations = recommender.scan_stocks()

        # Update cache
        global last_scan_results, last_scan_time
        last_scan_results = recommendations
        last_scan_time = datetime.now()

        return jsonify(recommendations)

    except Exception as e:
        logger.error(f"Error during manual scan: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sectors')
def get_sectors():
    """
    API endpoint to get trending sectors

    Returns:
        JSON with sector data
    """
    try:
        sectors = recommender.get_trending_sectors(top_n=10)
        return jsonify({'sectors': sectors})

    except Exception as e:
        logger.error(f"Error fetching sectors: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stock/<ticker>')
def get_stock_details(ticker):
    """
    API endpoint to get detailed analysis for a specific stock

    Args:
        ticker: Stock ticker symbol

    Returns:
        JSON with stock details
    """
    try:
        details = recommender.get_stock_details(ticker.upper())

        if details is None:
            return jsonify({'error': f'Unable to analyze {ticker}'}), 404

        return jsonify(details)

    except Exception as e:
        logger.error(f"Error getting stock details for {ticker}: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/send-email', methods=['POST'])
def send_email_report():
    """
    API endpoint to manually send email report

    Returns:
        JSON with status
    """
    try:
        # Use cached results or perform new scan
        recommendations = last_scan_results

        if recommendations is None:
            logger.info("No cached results, performing new scan...")
            recommendations = recommender.scan_stocks()

        # Send email
        success = email_reporter.send_stock_report(recommendations)

        if success:
            return jsonify({'success': True, 'message': 'Email sent successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to send email'}), 500

    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/status')
def get_status():
    """
    API endpoint to get system status

    Returns:
        JSON with system status
    """
    return jsonify({
        'status': 'active',
        'last_scan': last_scan_time.isoformat() if last_scan_time else None,
        'scheduler_running': scheduler.running,
        'next_scheduled_scan': '07:00 AM daily'
    })


def start_scheduler():
    """Start the background scheduler for daily reports"""
    try:
        # Schedule daily report at 7 AM
        scheduler.add_job(
            func=scheduled_scan_and_email,
            trigger=CronTrigger(hour=7, minute=0),
            id='daily_stock_scan',
            name='Daily Stock Scan and Email',
            replace_existing=True
        )

        scheduler.start()
        logger.info("Scheduler started successfully - Daily reports at 7:00 AM")

    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")


if __name__ == '__main__':
    # Start the scheduler
    start_scheduler()

    logger.info("Starting Stock Recommendation Flask Application...")
    logger.info("Access the web interface at http://localhost:5000")

    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
