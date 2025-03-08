from datetime import datetime
import numpy as np
import pandas as pd

from macd import MACD  # Import the MACD class
from back_test import backtest_strategy  # Import backtesting function
from plot_backtest import plot_results  # Import plotting function

# MACD Parameters
FAST_PERIOD = 12
SLOW_PERIOD = 26
SIGNAL_PERIOD = 9

# Initial Investment
INITIAL_CAPITAL = 10000.0


def run_macd_strategy(price_data, histogram_threshold=0, initial_capital=10000.0):
    """
    Run the MACD strategy end-to-end with improved parameters
    
    Parameters:
    price_data (pd.Series): Series of price data
    histogram_threshold (float): Minimum histogram value to confirm a signal
    initial_capital (float): Initial capital for the backtest
    
    Returns:
    pd.DataFrame: DataFrame with backtest results
    """
    # Instantiate MACD with predefined periods
    macd_indicator = MACD(FAST_PERIOD, SLOW_PERIOD, SIGNAL_PERIOD)

    # Calculate MACD
    macd_df = macd_indicator.calculate_macd(price_data)
    
    # Generate signals with improved filtering
    signals_df = macd_indicator.generate_signals(price_data, macd_df, histogram_threshold)
    
    # Backtest strategy
    backtest_df = backtest_strategy(signals_df, initial_capital)
    
    # Plot results
    plot_results(backtest_df)
    
    # Calculate additional performance metrics
    calculate_performance_metrics(backtest_df)
    
    # Return the backtest results
    return backtest_df

def calculate_performance_metrics(backtest_df):
    """
    Calculate additional performance metrics for the strategy
    
    Parameters:
    backtest_df (pd.DataFrame): DataFrame with backtest results
    
    Returns:
    dict: Dictionary with performance metrics
    """
    # Calculate daily returns
    backtest_df['Daily_Return'] = backtest_df['Portfolio'].pct_change()
    
    # Calculate annualized return
    total_days = (backtest_df.index[-1] - backtest_df.index[0]).days
    if total_days > 0:
        years = total_days / 365.25
        total_return = backtest_df['Portfolio'].iloc[-1] / backtest_df['Portfolio'].iloc[0] - 1
        annualized_return = (1 + total_return) ** (1 / years) - 1
    else:
        annualized_return = 0
    
    # Calculate maximum drawdown
    backtest_df['Cummax'] = backtest_df['Portfolio'].cummax()
    backtest_df['Drawdown'] = (backtest_df['Portfolio'] / backtest_df['Cummax'] - 1)
    max_drawdown = backtest_df['Drawdown'].min()
    
    # Calculate Sharpe ratio (assuming risk-free rate of 0)
    if len(backtest_df) > 1:
        sharpe_ratio = np.sqrt(252) * backtest_df['Daily_Return'].mean() / backtest_df['Daily_Return'].std()
    else:
        sharpe_ratio = 0
    
    metrics = {
        'Annualized Return': annualized_return * 100,
        'Max Drawdown': max_drawdown * 100,
        'Sharpe Ratio': sharpe_ratio
    }
    
    # Print metrics
    print(f"Annualized Return: {metrics['Annualized Return']:.2f}%")
    print(f"Maximum Drawdown: {metrics['Max Drawdown']:.2f}%")
    print(f"Sharpe Ratio: {metrics['Sharpe Ratio']:.2f}")
    
    return metrics

# Example usage
if __name__ == "__main__":
    # Generate some sample data for demonstration
    np.random.seed(42)
    dates = pd.date_range(start='2022-01-01', periods=252, freq='B')  # 252 business days = ~1 year
    
    # Create a simulated price series with some trend and randomness
    price = 100  # Starting price
    prices = [price]
    for _ in range(1, len(dates)):
        # Add some random walk with a slight upward bias
        change = np.random.normal(0.05, 1.0)  # Mean=0.05 (slight upward bias), SD=1.0
        price *= (1 + change/100)
        prices.append(price)
    
    # Create a Series with the generated prices
    price_data = pd.Series(prices, index=dates)
    
    # Run the MACD strategy
    results = run_macd_strategy(price_data)
    
    # Print final portfolio value and return
    final_portfolio = results['Portfolio'].iloc[-1]
    total_return = (final_portfolio / INITIAL_CAPITAL - 1) * 100
    
    print(f"Initial Capital: ${INITIAL_CAPITAL:.2f}")
    print(f"Final Portfolio Value: ${final_portfolio:.2f}")
    print(f"Total Return: {total_return:.2f}%")
    print(f"Number of Trades: {(results['Signal_Action'] != 0).sum()}")
