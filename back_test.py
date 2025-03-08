def backtest_strategy(signals_df, initial_capital=10000.0):
    """
    Backtest the MACD strategy
    
    Parameters:
    signals_df (pd.DataFrame): DataFrame with price data, MACD components, and signals
    initial_capital (float): Initial capital for the backtest
    
    Returns:
    pd.DataFrame: DataFrame with backtest results
    """
    # Create a copy of the signals DataFrame
    backtest_df = signals_df.copy()
    
    # Initialize position and portfolio columns
    backtest_df['Position'] = 0
    backtest_df['Portfolio'] = 0.0
    
    # Calculate positions (number of shares)
    # 1 means we're holding a long position, 0 means we have no position
    position = 0  # Start with no position
    
    for i in range(len(backtest_df)):
        if backtest_df['Signal_Action'].iloc[i] == 1:  # Buy signal
            position = 1
        elif backtest_df['Signal_Action'].iloc[i] == -1:  # Sell signal
            position = 0
        
        backtest_df.loc[backtest_df.index[i], 'Position'] = position
    
    # Calculate portfolio value
    # When position is 1, we have shares worth 'Price'
    # When position is 0, we have cash
    
    # First, calculate daily returns
    backtest_df['Daily_Return'] = backtest_df['Price'].pct_change()
    
    # Create a column for strategy returns based on position
    backtest_df['Strategy_Return'] = backtest_df['Position'].shift(1) * backtest_df['Daily_Return']
    backtest_df['Strategy_Return'].fillna(0, inplace=True)
    
    # Calculate cumulative portfolio value
    backtest_df['Portfolio'] = initial_capital * (1 + backtest_df['Strategy_Return']).cumprod()
    
    # Make sure first row portfolio value is initial capital
    backtest_df['Portfolio'].iloc[0] = initial_capital
    
    # Calculate cumulative returns
    backtest_df['Cumulative_Return'] = backtest_df['Portfolio'] / initial_capital
    
    return backtest_df
