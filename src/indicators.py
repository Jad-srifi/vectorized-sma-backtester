import pandas as pd

def calculate_SMA(close_price: pd.Series, period: int) -> pd.Series:
    if period <= 0:
        raise ValueError("Period should be strictly positive for the calculation of SMA")
    return close_price.rolling(period).mean()