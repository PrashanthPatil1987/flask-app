"""
Configuration file for Stock Recommendation Tool
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Email Configuration
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD', 'your-app-password')
    RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS', 'recipient@example.com').split(',')

    # Stock Filtering Criteria
    MIN_PRICE = 3.0  # Minimum stock price $3
    MIN_MARKET_CAP = 2_000_000_000  # $2 billion
    VOLUME_MULTIPLIER = 1.5  # Volume should be 1.5x average volume for breakout
    EMA_PERIOD = 50  # 50-day EMA

    # Scheduling
    REPORT_TIME = "07:00"  # 7 AM report time

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

    # Risk Management
    STOP_LOSS_PERCENT = 0.08  # 8% stop loss from buy price
    BUY_ZONE_PERCENT = 0.02  # 2% buy zone above current price
