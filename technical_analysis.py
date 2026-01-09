"""
Technical Analysis Module
Performs technical analysis including EMA, volume, and pattern detection
"""
import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import logging
from datetime import datetime, timedelta
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """Technical analysis for stock data"""

    def __init__(self, ema_period=50):
        self.ema_period = ema_period

    def get_stock_data(self, ticker, period='6mo'):
        """
        Fetch historical stock data using yfinance

        Args:
            ticker: Stock ticker symbol
            period: Time period (default 6 months)

        Returns:
            DataFrame with stock data
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)

            if df.empty:
                logger.warning(f"No data retrieved for {ticker}")
                return None

            return df

        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {e}")
            return None

    def calculate_ema(self, df, period=50):
        """Calculate Exponential Moving Average"""
        if df is None or df.empty:
            return None

        df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
        return df

    def calculate_volume_analysis(self, df):
        """
        Calculate volume analysis metrics

        Returns:
            DataFrame with volume indicators
        """
        if df is None or df.empty:
            return None

        # Average volume (20-day)
        df['Avg_Volume'] = df['Volume'].rolling(window=20).mean()

        # Volume ratio (current vs average)
        df['Volume_Ratio'] = df['Volume'] / df['Avg_Volume']

        # Volume breakout flag
        df['High_Volume'] = df['Volume_Ratio'] > Config.VOLUME_MULTIPLIER

        return df

    def calculate_rsi(self, df, period=14):
        """Calculate Relative Strength Index"""
        if df is None or df.empty:
            return None

        df['RSI'] = ta.rsi(df['Close'], length=period)
        return df

    def calculate_macd(self, df):
        """Calculate MACD indicator"""
        if df is None or df.empty:
            return None

        macd = ta.macd(df['Close'])
        if macd is not None:
            df = pd.concat([df, macd], axis=1)
        return df

    def detect_bullish_reversal(self, df):
        """
        Detect bullish reversal patterns

        Criteria:
        - Price was in downtrend
        - RSI oversold (< 40) then moving up
        - Price crossed above EMA
        - Increased volume

        Returns:
            Boolean indicating bullish reversal
        """
        if df is None or df.empty or len(df) < 50:
            return False

        try:
            recent = df.tail(5)
            current = df.iloc[-1]
            prev = df.iloc[-2]

            # Check if price is above 50 EMA
            above_ema = current['Close'] > current[f'EMA_{self.ema_period}']

            # Check RSI reversal (was oversold, now recovering)
            rsi_reversal = False
            if 'RSI' in df.columns:
                rsi_current = current['RSI']
                rsi_prev = prev['RSI']
                rsi_reversal = (rsi_prev < 40) and (rsi_current > rsi_prev)

            # Check price action (recent upward move)
            price_up = current['Close'] > prev['Close']

            # Check volume increase
            volume_increase = False
            if 'Volume_Ratio' in df.columns:
                volume_increase = current['Volume_Ratio'] > 1.2

            # Bullish reversal if multiple conditions met
            return above_ema and price_up and (rsi_reversal or volume_increase)

        except Exception as e:
            logger.error(f"Error detecting bullish reversal: {e}")
            return False

    def detect_bullish_breakout(self, df):
        """
        Detect bullish breakout patterns

        Criteria:
        - Price breaks above resistance (recent high)
        - Above 50 EMA
        - High volume on breakout
        - Strong momentum

        Returns:
            Boolean indicating bullish breakout
        """
        if df is None or df.empty or len(df) < 50:
            return False

        try:
            current = df.iloc[-1]
            recent_20 = df.tail(20)

            # Check if price is above 50 EMA
            above_ema = current['Close'] > current[f'EMA_{self.ema_period}']

            # Check breakout above recent resistance
            resistance = recent_20['High'].iloc[:-1].max()
            breakout = current['Close'] > resistance

            # Check high volume
            high_volume = False
            if 'High_Volume' in df.columns:
                high_volume = current['High_Volume']

            # Check positive price momentum
            price_momentum = current['Close'] > df['Close'].iloc[-5]

            return above_ema and breakout and high_volume and price_momentum

        except Exception as e:
            logger.error(f"Error detecting bullish breakout: {e}")
            return False

    def analyze_stock(self, ticker):
        """
        Comprehensive technical analysis for a stock

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with analysis results
        """
        try:
            # Fetch stock data
            df = self.get_stock_data(ticker)
            if df is None or df.empty:
                return None

            # Calculate all indicators
            df = self.calculate_ema(df, self.ema_period)
            df = self.calculate_volume_analysis(df)
            df = self.calculate_rsi(df)
            df = self.calculate_macd(df)

            current = df.iloc[-1]

            # Pattern detection
            is_bullish_reversal = self.detect_bullish_reversal(df)
            is_bullish_breakout = self.detect_bullish_breakout(df)

            # Calculate support and resistance
            recent_20 = df.tail(20)
            support = recent_20['Low'].min()
            resistance = recent_20['High'].max()

            analysis = {
                'ticker': ticker,
                'current_price': round(current['Close'], 2),
                'ema_50': round(current[f'EMA_{self.ema_period}'], 2),
                'above_ema': current['Close'] > current[f'EMA_{self.ema_period}'],
                'volume': int(current['Volume']),
                'avg_volume': int(current['Avg_Volume']) if 'Avg_Volume' in current else 0,
                'volume_ratio': round(current['Volume_Ratio'], 2) if 'Volume_Ratio' in current else 0,
                'rsi': round(current['RSI'], 2) if 'RSI' in current else None,
                'is_bullish_reversal': is_bullish_reversal,
                'is_bullish_breakout': is_bullish_breakout,
                'support': round(support, 2),
                'resistance': round(resistance, 2),
                'date': current.name.strftime('%Y-%m-%d')
            }

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing stock {ticker}: {e}")
            return None

    def calculate_buy_stop_levels(self, ticker, current_price=None):
        """
        Calculate suggested buy price and stop loss

        Args:
            ticker: Stock ticker symbol
            current_price: Current stock price (optional)

        Returns:
            Dictionary with buy and stop loss levels
        """
        try:
            if current_price is None:
                df = self.get_stock_data(ticker, period='1mo')
                if df is None or df.empty:
                    return None
                current_price = df.iloc[-1]['Close']

            # Buy zone: within 2% of current price
            buy_price_low = current_price * (1 - Config.BUY_ZONE_PERCENT)
            buy_price_high = current_price * (1 + Config.BUY_ZONE_PERCENT)

            # Stop loss: 8% below buy price
            stop_loss = current_price * (1 - Config.STOP_LOSS_PERCENT)

            return {
                'current_price': round(current_price, 2),
                'buy_price_low': round(buy_price_low, 2),
                'buy_price_high': round(buy_price_high, 2),
                'stop_loss': round(stop_loss, 2),
                'risk_percent': Config.STOP_LOSS_PERCENT * 100
            }

        except Exception as e:
            logger.error(f"Error calculating buy/stop levels for {ticker}: {e}")
            return None
