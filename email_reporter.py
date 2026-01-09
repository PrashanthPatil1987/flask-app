"""
Email Report Generator
Generates and sends HTML email reports with stock recommendations
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailReporter:
    """Email report generator and sender"""

    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.sender_email = Config.SENDER_EMAIL
        self.sender_password = Config.SENDER_PASSWORD
        self.recipient_emails = Config.RECIPIENT_EMAILS

    def generate_html_report(self, recommendations):
        """
        Generate HTML formatted email report

        Args:
            recommendations: Dictionary with stock recommendations

        Returns:
            HTML string
        """
        today = datetime.now().strftime('%B %d, %Y')

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #f4f4f4;
                }}
                .container {{
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #3498db;
                    margin-top: 30px;
                    border-left: 4px solid #3498db;
                    padding-left: 10px;
                }}
                .sector-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                .sector-card {{
                    background: #ecf0f1;
                    padding: 15px;
                    border-radius: 8px;
                    border-left: 4px solid #27ae60;
                }}
                .sector-card.negative {{
                    border-left-color: #e74c3c;
                }}
                .sector-name {{
                    font-weight: bold;
                    font-size: 14px;
                    color: #2c3e50;
                }}
                .sector-perf {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #27ae60;
                    margin: 5px 0;
                }}
                .sector-perf.negative {{
                    color: #e74c3c;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background: white;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: bold;
                }}
                td {{
                    padding: 10px;
                    border-bottom: 1px solid #ddd;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .ticker {{
                    font-weight: bold;
                    color: #2c3e50;
                    font-size: 16px;
                }}
                .price {{
                    color: #27ae60;
                    font-weight: bold;
                }}
                .buy-zone {{
                    background-color: #d5f4e6;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                .stop-loss {{
                    background-color: #fadbd8;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-weight: bold;
                }}
                .volume-high {{
                    color: #e67e22;
                    font-weight: bold;
                }}
                .recommendation {{
                    font-style: italic;
                    color: #7f8c8d;
                }}
                .no-stocks {{
                    padding: 20px;
                    text-align: center;
                    color: #7f8c8d;
                    font-style: italic;
                }}
                .footer {{
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 2px solid #ecf0f1;
                    color: #7f8c8d;
                    font-size: 12px;
                    text-align: center;
                }}
                .disclaimer {{
                    background-color: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📈 Stock Recommendations Report</h1>
                <p><strong>Date:</strong> {today}</p>

                <h2>🔥 Trending Sectors</h2>
                {self._generate_sector_section(recommendations.get('trending_sectors', []))}

                <h2>🚀 Bullish Breakouts</h2>
                {self._generate_stock_table(recommendations.get('bullish_breakouts', []))}

                <h2>🔄 Bullish Reversals</h2>
                {self._generate_stock_table(recommendations.get('bullish_reversals', []))}

                <h2>📊 High Volume Breakouts</h2>
                {self._generate_stock_table(recommendations.get('high_volume_breakouts', []))}

                <div class="disclaimer">
                    <strong>⚠️ Disclaimer:</strong> This report is for informational purposes only.
                    It is not financial advice. Always do your own research and consult with a
                    financial advisor before making investment decisions.
                </div>

                <div class="footer">
                    <p>Generated by Stock Recommendation Tool</p>
                    <p>Powered by Finviz.com data and Technical Analysis</p>
                </div>
            </div>
        </body>
        </html>
        """

        return html

    def _generate_sector_section(self, sectors):
        """Generate HTML for sector performance section"""
        if not sectors:
            return '<div class="no-stocks">No sector data available</div>'

        sector_html = '<div class="sector-grid">'

        for sector in sectors:
            perf = sector.get('performance_day', 0)
            is_negative = perf < 0
            card_class = 'sector-card negative' if is_negative else 'sector-card'
            perf_class = 'sector-perf negative' if is_negative else 'sector-perf'

            sector_html += f"""
            <div class="{card_class}">
                <div class="sector-name">{sector.get('name', 'N/A')}</div>
                <div class="{perf_class}">{perf:+.2f}%</div>
                <div style="font-size: 12px; color: #7f8c8d;">
                    Week: {sector.get('performance_week', 'N/A')}<br>
                    Month: {sector.get('performance_month', 'N/A')}
                </div>
            </div>
            """

        sector_html += '</div>'
        return sector_html

    def _generate_stock_table(self, stocks):
        """Generate HTML table for stock recommendations"""
        if not stocks:
            return '<div class="no-stocks">No stocks found matching criteria</div>'

        table_html = """
        <table>
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Current Price</th>
                    <th>Buy Zone</th>
                    <th>Stop Loss</th>
                    <th>Volume Ratio</th>
                    <th>RSI</th>
                    <th>Recommendation</th>
                </tr>
            </thead>
            <tbody>
        """

        for stock in stocks[:15]:  # Limit to top 15 stocks
            ticker = stock.get('ticker', 'N/A')
            current_price = stock.get('current_price', 0)
            buy_low = stock.get('buy_price_low', 0)
            buy_high = stock.get('buy_price_high', 0)
            stop_loss = stock.get('stop_loss', 0)
            volume_ratio = stock.get('volume_ratio', 0)
            rsi = stock.get('rsi', 'N/A')
            recommendation = stock.get('recommendation', '')

            rsi_display = f"{rsi:.1f}" if isinstance(rsi, (int, float)) else rsi

            table_html += f"""
            <tr>
                <td class="ticker">{ticker}</td>
                <td class="price">${current_price:.2f}</td>
                <td class="buy-zone">${buy_low:.2f} - ${buy_high:.2f}</td>
                <td class="stop-loss">${stop_loss:.2f}</td>
                <td class="volume-high">{volume_ratio:.2f}x</td>
                <td>{rsi_display}</td>
                <td class="recommendation">{recommendation}</td>
            </tr>
            """

        table_html += """
            </tbody>
        </table>
        """

        return table_html

    def send_email(self, subject, html_content, recipients=None):
        """
        Send email report

        Args:
            subject: Email subject
            html_content: HTML content of email
            recipients: List of recipient emails (optional, uses config if not provided)

        Returns:
            Boolean indicating success
        """
        if recipients is None:
            recipients = self.recipient_emails

        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = ', '.join(recipients)

            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)

            # Connect to SMTP server and send
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            logger.info(f"Email sent successfully to {', '.join(recipients)}")
            return True

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return False

    def send_stock_report(self, recommendations):
        """
        Generate and send stock recommendation report

        Args:
            recommendations: Dictionary with stock recommendations

        Returns:
            Boolean indicating success
        """
        try:
            today = datetime.now().strftime('%B %d, %Y')
            subject = f"📈 Stock Recommendations - {today}"

            html_content = self.generate_html_report(recommendations)

            return self.send_email(subject, html_content)

        except Exception as e:
            logger.error(f"Error sending stock report: {e}")
            return False
