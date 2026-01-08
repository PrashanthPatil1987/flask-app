"""
Finviz Scraper Module
Fetches stock data, sector information, and screening results from Finviz
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from finvizfinance.screener.overview import Overview
from finvizfinance.group.overview import Group
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinvizScraper:
    """Scraper for fetching stock data from Finviz"""

    def __init__(self):
        self.base_url = "https://finviz.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_trending_sectors(self):
        """
        Get trending sector groups from Finviz
        Returns DataFrame with sector performance
        """
        try:
            group = Group()
            # Get sector performance
            sector_data = group.ScreenerView(group='Sector', order='Performance (Day)')
            logger.info(f"Retrieved {len(sector_data)} sector groups")
            return sector_data
        except Exception as e:
            logger.error(f"Error fetching sector data: {e}")
            return pd.DataFrame()

    def get_industry_performance(self):
        """Get industry performance data"""
        try:
            group = Group()
            industry_data = group.ScreenerView(group='Industry', order='Performance (Day)')
            logger.info(f"Retrieved {len(industry_data)} industries")
            return industry_data
        except Exception as e:
            logger.error(f"Error fetching industry data: {e}")
            return pd.DataFrame()

    def screen_stocks(self, filters=None):
        """
        Screen stocks based on custom filters

        Args:
            filters: Dictionary of filter criteria

        Returns:
            DataFrame of filtered stocks
        """
        try:
            foverview = Overview()

            # Default filters for bullish setups
            if filters is None:
                filters = {
                    'Price': 'Over $3',
                    'Market Cap.': '+Mid (over $2bln)',
                    'Relative Volume': 'Over 1.5',
                    'Change': 'Up',
                }

            # Set filters
            foverview.set_filter(filters_dict=filters)

            # Get screener results
            df = foverview.screener_view()

            logger.info(f"Screened {len(df)} stocks with filters: {filters}")
            return df

        except Exception as e:
            logger.error(f"Error screening stocks: {e}")
            return pd.DataFrame()

    def get_bullish_breakout_stocks(self):
        """
        Get stocks showing bullish breakout patterns
        """
        filters = {
            'Price': 'Over $3',
            'Market Cap.': '+Mid (over $2bln)',
            'Relative Volume': 'Over 1.5',
            'Pattern': 'Horizontal S/R (Strong)',
            'Change': 'Up',
            '50-Day Simple Moving Average': 'Price above SMA50',
        }

        return self.screen_stocks(filters)

    def get_bullish_reversal_stocks(self):
        """
        Get stocks showing bullish reversal patterns
        """
        filters = {
            'Price': 'Over $3',
            'Market Cap.': '+Mid (over $2bln)',
            'Relative Volume': 'Over 1.5',
            'Pattern': 'Channel Up',
            'Change': 'Up',
            '50-Day Simple Moving Average': 'Price above SMA50',
            'RSI (14)': 'Oversold (30)',
        }

        return self.screen_stocks(filters)

    def get_high_volume_breakouts(self):
        """
        Get stocks with high volume breakouts
        """
        filters = {
            'Price': 'Over $3',
            'Market Cap.': '+Mid (over $2bln)',
            'Relative Volume': 'Over 2',
            'Change': 'Up 5%',
            'Volume': 'Over 2M',
            '50-Day Simple Moving Average': 'Price above SMA50',
        }

        return self.screen_stocks(filters)

    def get_stock_quote(self, ticker):
        """
        Get detailed quote for a specific ticker

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with stock details
        """
        try:
            url = f"{self.base_url}/quote.ashx?t={ticker}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Parse stock data from the page
                # This is a simplified version - can be expanded
                return {'ticker': ticker, 'url': url}
            else:
                logger.error(f"Failed to fetch quote for {ticker}")
                return None

        except Exception as e:
            logger.error(f"Error fetching quote for {ticker}: {e}")
            return None
