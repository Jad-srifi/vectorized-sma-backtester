from src.data_engine import generate_market_data
from src.signals import generate_signal_SMA, execute_signal_SMA, strategy_return_SMA
from src.analysis import cumulative_return, visualize_backtest, strategy_cumulative_return_SMA

if __name__ == "__main__":
    # 1. Ingest Data
    data = generate_market_data()
    price = data['close_price']

    # 2. Generate and Shift Signals
    signal = generate_signal_SMA(price, 10, 50)
    shifted_signal = execute_signal_SMA(signal)

    # 3. Calculate Returns
    asset_returns = price.pct_change()
    strat_returns = strategy_return_SMA(asset_returns, shifted_signal)

    # 4. Aggregate and Visualize
    asset_growth = cumulative_return(asset_returns)
    strat_growth = strategy_cumulative_return_SMA(strat_returns)

    visualize_backtest(asset_growth, strat_growth)