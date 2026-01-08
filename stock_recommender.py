"""
Stock Recommendation Engine
Combines finviz data, technical analysis, and filtering to generate stock recommendations
"""
import pandas as pd
import logging
from finviz_scraper import FinvizScraper
from technical_analysis import TechnicalAnalyzer
from config import Config
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockRecommender:
    """Main stock recommendation engine"""

    def __init__(self):
        self.scraper = FinvizScraper()
        self.analyzer = TechnicalAnalyzer(ema_period=Config.EMA_PERIOD)

    def get_trending_sectors(self, top_n=5):
        """
        Get top performing sectors

        Args:
            top_n: Number of top sectors to return

        Returns:
            List of dictionaries with sector information
        """
        try:
            sector_df = self.scraper.get_trending_sectors()

            if sector_df is None or sector_df.empty:
                return []

            # Sort by performance and get top N
            if 'Performance (Day)' in sector_df.columns:
                sector_df['Performance (Day)'] = sector_df['Performance (Day)'].str.rstrip('%').astype(float)
                sector_df = sector_df.sort_values('Performance (Day)', ascending=False).head(top_n)

            sectors = []
            for _, row in sector_df.iterrows():
                sector_info = {
                    'name': row.get('Name', 'N/A'),
                    'performance_day': row.get('Performance (Day)', 0),
                    'performance_week': row.get('Performance (Week)', 'N/A'),
                    'performance_month': row.get('Performance (Month)', 'N/A'),
                    'stocks': row.get('Stocks', 'N/A'),
                }
                sectors.append(sector_info)

            return sectors

        except Exception as e:
            logger.error(f"Error getting trending sectors: {e}")
            return []

    def scan_stocks(self):
        """
        Main stock scanning function
        Combines finviz screening and technical analysis

        Returns:
            Dictionary with recommendations categorized by pattern type
        """
        logger.info("Starting stock scan...")

        recommendations = {
            'bullish_breakouts': [],
            'bullish_reversals': [],
            'high_volume_breakouts': [],
            'trending_sectors': []
        }

        try:
            # Get trending sectors
            logger.info("Fetching trending sectors...")
            recommendations['trending_sectors'] = self.get_trending_sectors(top_n=5)

            # Get bullish breakout stocks
            logger.info("Screening for bullish breakouts...")
            breakout_stocks = self.scraper.get_bullish_breakout_stocks()
            if not breakout_stocks.empty:
                recommendations['bullish_breakouts'] = self._analyze_stock_list(
                    breakout_stocks, 'breakout'
                )

            # Get bullish reversal stocks
            logger.info("Screening for bullish reversals...")
            reversal_stocks = self.scraper.get_bullish_reversal_stocks()
            if not reversal_stocks.empty:
                recommendations['bullish_reversals'] = self._analyze_stock_list(
                    reversal_stocks, 'reversal'
                )

            # Get high volume breakouts
            logger.info("Screening for high volume breakouts...")
            volume_stocks = self.scraper.get_high_volume_breakouts()
            if not volume_stocks.empty:
                recommendations['high_volume_breakouts'] = self._analyze_stock_list(
                    volume_stocks, 'volume_breakout'
                )

            logger.info("Stock scan completed successfully")

        except Exception as e:
            logger.error(f"Error during stock scan: {e}")

        return recommendations

    def _analyze_stock_list(self, stock_df, pattern_type, max_stocks=10):
        """
        Analyze a list of stocks with technical analysis

        Args:
            stock_df: DataFrame of stocks from finviz
            pattern_type: Type of pattern (breakout, reversal, volume_breakout)
            max_stocks: Maximum number of stocks to analyze

        Returns:
            List of analyzed stocks with recommendations
        """
        analyzed_stocks = []

        if stock_df.empty:
            return analyzed_stocks

        # Get tickers (limit to max_stocks for performance)
        tickers = stock_df['Ticker'].head(max_stocks).tolist()

        logger.info(f"Analyzing {len(tickers)} stocks for {pattern_type}...")

        # Parallel processing for faster analysis
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_ticker = {
                executor.submit(self._analyze_single_stock, ticker, pattern_type): ticker
                for ticker in tickers
            }

            for future in as_completed(future_to_ticker):
                result = future.result()
                if result is not None:
                    analyzed_stocks.append(result)

        # Sort by volume ratio (highest first)
        analyzed_stocks.sort(key=lambda x: x.get('volume_ratio', 0), reverse=True)

        return analyzed_stocks

    def _analyze_single_stock(self, ticker, pattern_type):
        """
        Analyze a single stock with technical indicators

        Args:
            ticker: Stock ticker symbol
            pattern_type: Pattern type being analyzed

        Returns:
            Dictionary with stock analysis or None if analysis fails
        """
        try:
            # Perform technical analysis
            analysis = self.analyzer.analyze_stock(ticker)

            if analysis is None:
                return None

            # Apply additional filtering
            if not self._meets_criteria(analysis):
                return None

            # Calculate buy and stop loss levels
            levels = self.analyzer.calculate_buy_stop_levels(
                ticker, analysis['current_price']
            )

            if levels is None:
                return None

            # Combine analysis with buy/stop levels
            recommendation = {
                **analysis,
                **levels,
                'pattern_type': pattern_type,
                'recommendation': self._generate_recommendation(analysis, pattern_type)
            }

            logger.info(f"✓ {ticker}: ${analysis['current_price']} - {pattern_type}")

            return recommendation

        except Exception as e:
            logger.error(f"Error analyzing {ticker}: {e}")
            return None

    def _meets_criteria(self, analysis):
        """
        Check if stock meets all filtering criteria

        Args:
            analysis: Dictionary with stock analysis

        Returns:
            Boolean indicating if criteria are met
        """
        # Must be above 50 EMA
        if not analysis.get('above_ema', False):
            return False

        # Current price must be above minimum
        if analysis.get('current_price', 0) < Config.MIN_PRICE:
            return False

        return True

    def _generate_recommendation(self, analysis, pattern_type):
        """
        Generate recommendation text based on analysis

        Args:
            analysis: Stock analysis dictionary
            pattern_type: Pattern type

        Returns:
            Recommendation string
        """
        ticker = analysis['ticker']
        price = analysis['current_price']
        pattern = pattern_type.replace('_', ' ').title()

        if analysis.get('is_bullish_breakout'):
            return f"{ticker} showing strong {pattern} - High conviction buy"
        elif analysis.get('is_bullish_reversal'):
            return f"{ticker} in {pattern} pattern - Good entry opportunity"
        else:
            return f"{ticker} meeting {pattern} criteria - Monitor for entry"

    def get_stock_details(self, ticker):
        """
        Get detailed analysis for a specific stock

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with detailed stock information
        """
        try:
            analysis = self.analyzer.analyze_stock(ticker)
            if analysis is None:
                return None

            levels = self.analyzer.calculate_buy_stop_levels(ticker)

            return {
                **analysis,
                **levels,
                'recommendation': self._generate_recommendation(analysis, 'detailed_analysis')
            }

        except Exception as e:
            logger.error(f"Error getting details for {ticker}: {e}")
            return None
