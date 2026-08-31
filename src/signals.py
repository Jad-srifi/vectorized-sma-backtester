import pandas as pd
from .indicators import calculate_SMA

def generate_signal_SMA(close_price: pd.Series, fast_window: int, slow_window: int) -> pd.Series:
    """t1 is early date lower date, t2 is older date"""
    t1_sma = calculate_SMA(close_price, fast_window)
    t2_sma = calculate_SMA(close_price, slow_window)
    
    return (t1_sma > t2_sma).astype(int)

def execute_signal_SMA(signal: pd.Series) -> pd.Series:
    return signal.shift(1)

def strategy_return_SMA(returns: pd.Series, signal: pd.Series) -> pd.Series:
    return signal * returns