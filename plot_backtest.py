import matplotlib.pyplot as plt

def plot_results(backtest_df):
    """
    Plot the backtest results
    
    Parameters:
    backtest_df (pd.DataFrame): DataFrame with backtest results
    
    Returns:
    None
    """
    # Create a 2x2 subplot
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 14), sharex=True)
    
    # Plot the price and buy/sell signals
    ax1.plot(backtest_df.index, backtest_df['Price'], label='Price')
    ax1.plot(backtest_df.loc[backtest_df['Signal_Action'] == 1].index, 
            backtest_df.loc[backtest_df['Signal_Action'] == 1]['Price'], 
            '^', markersize=10, color='g', label='Buy Signal')
    ax1.plot(backtest_df.loc[backtest_df['Signal_Action'] == -1].index, 
            backtest_df.loc[backtest_df['Signal_Action'] == -1]['Price'], 
            'v', markersize=10, color='r', label='Sell Signal')
    ax1.set_title('Price and Buy/Sell Signals')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True)
    
    # Plot the MACD and Signal line
    ax2.plot(backtest_df.index, backtest_df['MACD'], label='MACD', color='blue')
    ax2.plot(backtest_df.index, backtest_df['Signal'], label='Signal Line', color='red')
    ax2.bar(backtest_df.index, backtest_df['Histogram'], label='Histogram', color='green', alpha=0.5)
    ax2.set_title('MACD, Signal Line, and Histogram')
    ax2.set_ylabel('MACD')
    ax2.legend()
    ax2.grid(True)
    
    # Plot the portfolio value
    ax3.plot(backtest_df.index, backtest_df['Portfolio'], label='Portfolio Value', color='purple')
    ax3.set_title('Portfolio Value')
    ax3.set_ylabel('Portfolio Value ($)')
    ax3.set_xlabel('Date')
    ax3.legend()
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()