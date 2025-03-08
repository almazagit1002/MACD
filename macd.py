import pandas as pd
import numpy as np

class MACD:
    def __init__(self, fast_period, slow_period, signal_period):
        """
        Initialize the MACD class with given periods
        
        Parameters:
        fast_period (int): Period for the fast EMA
        slow_period (int): Period for the slow EMA
        signal_period (int): Period for the signal line
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
    
    def calculate_macd(self, price_data):
        """
        Calculate the MACD, MACD Signal, and MACD Histogram
        
        Parameters:
        price_data (pd.Series): Series of price data
        
        Returns:
        pd.DataFrame: DataFrame with MACD, MACD Signal, and MACD Histogram
        """
        # Calculate the fast and slow EMA
        ema_fast = price_data.ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = price_data.ewm(span=self.slow_period, adjust=False).mean()
        
        # Calculate the MACD line
        macd_line = ema_fast - ema_slow
        
        # Calculate the MACD signal line
        macd_signal = macd_line.ewm(span=self.signal_period, adjust=False).mean()
        
        # Calculate the MACD histogram
        macd_histogram = macd_line - macd_signal
        
        # Create and return a DataFrame with all the MACD components
        macd_df = pd.DataFrame({
            'MACD': macd_line,
            'Signal': macd_signal,
            'Histogram': macd_histogram
        })
        
        return macd_df

    def generate_signals(self, price_data, macd_df, histogram_threshold=0):
        """
        Generate buy and sell signals based on MACD strategy with improved filtering
        
        Parameters:
        price_data (pd.Series): Series of price data
        macd_df (pd.DataFrame): DataFrame with MACD, MACD Signal, and MACD Histogram
        histogram_threshold (float): Minimum histogram value to confirm a signal (reduces false signals)
        
        Returns:
        pd.DataFrame: DataFrame with price data, MACD components, and signals
        """
        # Create a copy of the price data
        signals_df = pd.DataFrame(price_data)
        signals_df.columns = ['Price']
        
        # Add the MACD components
        signals_df['MACD'] = macd_df['MACD']
        signals_df['Signal'] = macd_df['Signal']
        signals_df['Histogram'] = macd_df['Histogram']
        
        # Add a trend indicator (20-period SMA)
        signals_df['Trend'] = signals_df['Price'].rolling(window=20).mean()
        
        # Initialize the signal column
        signals_df['Signal_Action'] = 0
        
        # Generate signals with additional filtering
        # Buy signal (1) when:
        # - MACD crosses above the Signal line
        # - Histogram is above the threshold (optional)
        # - Price is above its 20-period SMA (trend filter)
        buy_condition = (
            (signals_df['MACD'] > signals_df['Signal']) & 
            (signals_df['MACD'].shift(1) <= signals_df['Signal'].shift(1)) &
            (signals_df['Histogram'] > histogram_threshold) &
            (signals_df['Price'] > signals_df['Trend'])
        )
        
        # Sell signal (-1) when:
        # - MACD crosses below the Signal line
        # - Histogram is below negative threshold (optional)
        # - Price is below its 20-period SMA (trend filter)
        sell_condition = (
            (signals_df['MACD'] < signals_df['Signal']) & 
            (signals_df['MACD'].shift(1) >= signals_df['Signal'].shift(1)) &
            (signals_df['Histogram'] < -histogram_threshold) &
            (signals_df['Price'] < signals_df['Trend'])
        )
        
        # Apply conditions
        signals_df.loc[buy_condition, 'Signal_Action'] = 1
        signals_df.loc[sell_condition, 'Signal_Action'] = -1
        
        return signals_df
