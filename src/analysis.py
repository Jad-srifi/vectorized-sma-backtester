import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def strategy_cumulative_return_SMA(strategy_returns: pd.Series) -> pd.Series:
    return (strategy_returns + 1).fillna(1).cumprod()

def cumulative_return(returns: pd.Series) -> pd.Series:
    return (1 + returns).cumprod()

def visualize_backtest(asset_growth: pd.Series, strategy_growth: pd.Series):
    days = np.arange(len(asset_growth))
    
    plt.plot(days, asset_growth, color='blue', label='Buy & Hold asset')
    plt.plot(days, strategy_growth, color='orange', label='SMA strategy')
    
    plt.legend()
    plt.show()
    