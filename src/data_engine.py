import pandas as pd
import numpy as np

def generate_market_data(days: int = 500, seed: int = 42) -> pd.DataFrame:
    """
    Synthesizes a random walk price series to simulate a market environment.
    Initializes at a baseline price of 100.
    """
    np.random.seed(seed)
    price_array = np.random.randn(days).cumsum() + 100
    
    return pd.DataFrame({'close_price': price_array})