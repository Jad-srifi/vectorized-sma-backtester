# Vectorized Backtest Pipeline: Eliminating Lookahead Bias

An institutional-grade, purely vectorized algorithmic trading backtester designed to process financial time-series data efficiently while preventing structural data leakage.

This project demonstrates the transition from theoretical trading logic to realistic market execution constraints. It implements a Moving Average Crossover strategy using vectorized Pandas operations and explicitly eliminates **lookahead bias** through a mandatory one-period execution delay.

---

## Executive Summary

A trading strategy's theoretical alpha is meaningless if the underlying backtesting pipeline allows the algorithm to access information that would not have been available at the time of execution.

This project addresses two fundamental problems in quantitative backtesting:

1. **Computational inefficiency** caused by row-by-row Python iteration.
2. **Lookahead bias** caused by executing trades using information from the same period in which the trade is assumed to occur.

The engine uses vectorized array operations throughout the data-processing and signal-generation pipeline. It generates synthetic market data, calculates moving averages, evaluates crossover signals, applies a strict $T+1$ execution delay, and compounds strategy returns into an equity curve.

The result is a modular backtesting pipeline designed around two principles:

> **Vectorize the mathematics.**
> **Respect the information available at execution time.**

---

## Features

* **Fully Vectorized Computation**
  Uses Pandas and NumPy array operations instead of row-by-row Python iteration.

* **Lookahead Bias Prevention**
  Applies a mandatory `.shift(1)` to convert theoretical signals into executable trading states.

* **Modular Architecture**
  Separates market generation, indicator calculation, signal evaluation, return analysis, and visualization.

* **Benchmark Comparison**
  Compares strategy performance against a passive buy-and-hold benchmark.

* **Equity Curve Construction**
  Compounds periodic returns into a continuous portfolio equity curve.

* **NaN-Safe Return Handling**
  Properly handles uninitialized rolling-window periods before cumulative compounding.

* **Deterministic Market Simulation**
  Generates reproducible synthetic price data for controlled experimentation.

---

## Project Architecture

```text
vectorized-backtester-sma/
│
├── main.py
│
├── src/
│   ├── data_engine.py
│   ├── indicators.py
│   ├── signals.py
│   └── analysis.py
│
├── requirements.txt
└── README.md
```

### `main.py`

The primary entry point and orchestration layer.

Responsible for:

* Running the complete backtesting pipeline
* Connecting the individual modules
* Triggering analysis and visualization

The file intentionally contains minimal mathematical logic.

---

### `src/data_engine.py`

Responsible for deterministic market simulation.

Generates synthetic random-walk price series that can be used to test the backtesting pipeline under controlled conditions.

---

### `src/indicators.py`

Contains the vectorized technical-indicator calculations.

Currently implements:

* Simple Moving Average (SMA)
* Rolling-window calculations

Example:

```python
df["SMA_10"] = df["price"].rolling(10).mean()
df["SMA_50"] = df["price"].rolling(50).mean()
```

These operations are performed across the entire array rather than through explicit Python iteration.

---

### `src/signals.py`

Contains the trading-state evaluation logic.

The module:

1. Compares the short and long moving averages.
2. Generates a binary trading state.
3. Applies the execution delay required to prevent lookahead bias.

Conceptually:

```text
Market Data
     │
     ▼
SMA Calculation
     │
     ▼
Raw Signal
     │
     ▼
shift(1)
     │
     ▼
Executable Signal
```

---

### `src/analysis.py`

Responsible for return transformations, equity-curve construction, and visualization.

It calculates:

* Asset returns
* Strategy returns
* Cumulative asset returns
* Cumulative strategy returns
* Performance visualizations

---

# Backtesting Pipeline

The complete pipeline follows this sequence:

```text
Synthetic Market Data
        │
        ▼
Price Series
        │
        ▼
Moving Averages
        │
        ▼
Raw Trading Signal
        │
        ▼
One-Period Execution Delay
        │
        ▼
Strategy Returns
        │
        ▼
Cumulative Equity Curve
        │
        ▼
Benchmark Comparison
        │
        ▼
Visualization
```

This separation makes it possible to replace individual components without rewriting the entire backtester.

---

# Visual Diagnostics

Running:

```bash
python main.py
```

generates the visual backtest analysis.

## Equity Curve Comparison

The primary diagnostic compares the strategy's cumulative performance against a passive buy-and-hold position.

The visualization allows the strategy's capital exposure and performance to be compared directly with the underlying asset.

### Example

**Synthetic Data**

![Equity Curve Comparison](https://github.com/user-attachments/assets/c463ae19-c149-4ca7-aa1c-4d616b938de7)

**BTC Data**

![Equity Curve Comparison](https://github.com/user-attachments/assets/54b6d4f3-aab9-4c8a-b47c-6d972e71c5c4)

> **Note:** The BTC dataset is **not included in this repository**. This example was generated using external BTC market data solely to validate and test the backtesting pipeline on real-world financial time-series data. The repository currently uses synthetic data for reproducibility.

---

# Installation

## Requirements

* Python 3.10+
* NumPy
* Pandas
* Matplotlib

Install the dependencies with:

```bash
pip install numpy pandas matplotlib
```

Or, if a `requirements.txt` file is provided:

```bash
pip install -r requirements.txt
```

---

# Usage

Clone the repository:

```bash
git clone https://github.com/Jad-srifi/vectorized-sma-backtester.git
```

Navigate into the project:

```bash
cd vectorized-sma-backtester
```

Run the backtest:

```bash
python main.py
```

---

# Mathematical Foundations

## Simple Moving Averages

The strategy uses two Simple Moving Averages:

### 10-Period SMA

$$SMA_{10,t}=\frac{1}{10}\sum_{i=0}^{9} P_{t-i}$$

### 50-Period SMA

$$SMA_{50,t}=\frac{1}{50}\sum_{i=0}^{49} P_{t-i}$$

where:

* $P_t$ is the asset price at time $t$
* $SMA_{10,t}$ is the short-term moving average
* $SMA_{50,t}$ is the long-term moving average

---

## Raw Trading Signal

The raw signal determines whether the short-term moving average is above the long-term moving average:

$$S_{raw,t}=\begin{cases}1, & \text{if } SMA_{10,t} > SMA_{50,t} \\0, & \text{otherwise}\end{cases}$$

A value of:

* $1$ means the strategy is exposed to the asset.
* $0$ means the strategy holds no position.

---

# Lookahead Bias Prevention

This is the central structural constraint of the project.

Suppose the moving averages at time $t$ are calculated using the closing price $P_t$.

The strategy **cannot simultaneously use that information to make a trade at the same closing price** unless the execution model explicitly assumes that information and execution occur after the close.

To prevent this, the raw signal is shifted forward by one period:

$$S_{exec,t}=S_{raw,t-1}$$

In Pandas:

```python
df["signal_exec"] = df["signal_raw"].shift(1)
```

Therefore:

```text
Information available at T
          │
          ▼
Signal generated at T
          │
          ▼
Trade executed at T+1
```

This enforces the information constraint:

$$\text{Decision}_{t}\subseteq\text{Information}_{t-1}$$

The strategy therefore cannot use information from the current period to determine the current-period position.

---

# Strategy Returns

Once the executable signal has been generated, strategy returns are calculated through element-wise multiplication:

$$R_{strat,t}=S_{exec,t}\cdot R_t$$

where:

* $R_t$ is the asset return at time $t$
* $S_{exec,t}$ is the executable position
* $R_{strat,t}$ is the strategy return

In vectorized form:

```python
df["strategy_return"] = (
    df["signal_exec"] * df["asset_return"]
)
```

No explicit Python loop is required.

---

# Equity Curve

Periodic returns are converted into cumulative portfolio growth using:

$$E_t=\prod_{i=1}^{t}(1 + R_{strat,i})$$

In Pandas:

```python
df["strategy_equity"] = (
    1 + df["strategy_return"]
).cumprod()
```

The same transformation is applied to the passive benchmark:

```python
df["asset_equity"] = (
    1 + df["asset_return"]
).cumprod()
```

---

# Handling NaN Values

Rolling indicators naturally produce undefined values at the beginning of the dataset.

For example, a 50-period SMA cannot be calculated until at least 50 observations exist.

These values must be handled carefully.

A critical distinction is made between:

```text
Return = 0
```

and:

```text
Growth multiplier = 1
```

For cumulative compounding:

$$1 + 0 = 1$$

Therefore, an unexposed or undefined return period should preserve the portfolio's existing capital rather than introduce a zero multiplier.

Incorrect:

```python
df["strategy_return"].fillna(0).cumprod()
```

Correct conceptual approach:

```python
growth = 1 + df["strategy_return"]
growth = growth.fillna(1.0)

equity = growth.cumprod()
```

A zero multiplier would destroy the entire cumulative equity curve:

$$E_t \times 0 = 0$$

Once cumulative capital reaches zero, every subsequent product remains zero.

---

# Design Constraints

## 1. Vectorization Mandate

Explicit row-by-row iteration is intentionally avoided.

Forbidden for core numerical operations:

```python
for index, row in df.iterrows():
    ...
```

Instead, operations are expressed as array transformations:

```python
df["SMA_10"] = df["price"].rolling(10).mean()
df["SMA_50"] = df["price"].rolling(50).mean()
```

The objective is to delegate numerical operations to optimized Pandas/NumPy implementations rather than repeatedly invoking the Python interpreter.

---

## 2. Information-Set Integrity

A backtest must distinguish between:

```text
What was known?
```

and:

```text
When was the trade executable?
```

Using a signal calculated from $P_t$ to execute at $P_t$ introduces a temporal inconsistency unless the execution model explicitly supports it.

This project therefore enforces:

$$S_{exec,t} = S_{raw,t-1}$$

---

## 3. No Artificial Capital Destruction

Undefined or inactive periods must not introduce artificial losses into the equity curve.

The portfolio state is preserved using a neutral growth multiplier:

$$1.0$$

rather than:

$$0.0$$

---

# Key Lessons

### Backtesting Is a Data-Integrity Problem

A sophisticated strategy cannot compensate for a flawed data pipeline.

If future information leaks into historical decisions, the resulting performance statistics are meaningless.

---

### Vectorization Is a Computational Design Choice

Vectorization is not simply a stylistic preference. It changes where computation occurs.

Instead of:

```text
Python
  │
  ├── Row 1
  ├── Row 2
  ├── Row 3
  ├── ...
  └── Row N
```

the pipeline operates on entire arrays:

```text
Python
   │
   ▼
Pandas / NumPy
   │
   ▼
Vectorized Array Operations
```

---

### Execution Assumptions Matter

A backtest does not merely ask:

> "Would this signal have been profitable?"

It must ask:

> "Could this trade actually have been executed using the information available at that time?"

That distinction separates a mathematical experiment from a meaningful trading simulation.

---

# Current Strategy

The current implementation uses a simple Moving Average Crossover:

```text
SMA(10) > SMA(50)
        │
        ▼
     Long
```

Otherwise:

```text
SMA(10) ≤ SMA(50)
        │
        ▼
      Flat
```

The strategy is intentionally simple. Its purpose is not to demonstrate sophisticated alpha generation, but to establish a structurally sound foundation for future research.

---

# Future Extensions

Potential extensions include:

* Transaction costs
* Bid/ask spread modeling
* Slippage
* Position sizing
* Stop-loss and take-profit logic
* Volatility targeting
* Sharpe ratio
* Maximum drawdown
* Sortino ratio
* Value at Risk (VaR)
* Parameter optimization
* Walk-forward validation
* Out-of-sample testing
* Multiple assets
* Portfolio-level backtesting
* Event-driven execution simulation
* Market microstructure modeling
* Real market data integration

These additions should preserve the same fundamental constraint:

$$\boxed{\text{No decision may depend on information unavailable at execution time.}}$$

---

# Disclaimer

This project is an educational and research-oriented backtesting framework. Synthetic data and simplified execution assumptions do not represent actual market conditions.

Backtested performance does not guarantee future results.
