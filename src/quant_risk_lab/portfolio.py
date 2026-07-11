import numpy as np
import pandas as pd

from config import PROCESSED_DATA_DIR
from risk_metrics import (
    TRADING_DAYS_PER_YEAR,
    RISK_FREE_RATE,
    load_returns,
    compute_annualized_return,
    compute_annualized_volatility,
    compute_cumulative_returns,
    compute_drawdowns,
    compute_max_drawdown,
    compute_sharpe_ratio,
    compute_sortino_ratio,
    compute_historical_var,
    compute_historical_cvar,
)


DEFAULT_PORTFOLIOS = {
    "Equal Weight": {
        "AAPL": 0.125,
        "MSFT": 0.125,
        "NVDA": 0.125,
        "JPM": 0.125,
        "XOM": 0.125,
        "SPY": 0.125,
        "TLT": 0.125,
        "GLD": 0.125,
    },
    "Equity Heavy": {
        "AAPL": 0.15,
        "MSFT": 0.15,
        "NVDA": 0.15,
        "JPM": 0.10,
        "XOM": 0.10,
        "SPY": 0.25,
        "TLT": 0.05,
        "GLD": 0.05,
    },
    "Defensive": {
        "AAPL": 0.05,
        "MSFT": 0.05,
        "NVDA": 0.00,
        "JPM": 0.00,
        "XOM": 0.00,
        "SPY": 0.30,
        "TLT": 0.35,
        "GLD": 0.25,
    },
    "Growth Tech": {
        "AAPL": 0.25,
        "MSFT": 0.25,
        "NVDA": 0.25,
        "JPM": 0.00,
        "XOM": 0.00,
        "SPY": 0.15,
        "TLT": 0.05,
        "GLD": 0.05,
    },
    "Balanced": {
        "AAPL": 0.10,
        "MSFT": 0.10,
        "NVDA": 0.05,
        "JPM": 0.05,
        "XOM": 0.05,
        "SPY": 0.35,
        "TLT": 0.20,
        "GLD": 0.10,
    },
}


def weights_to_series(
    weights: dict[str, float],
    asset_names: list[str],
) -> pd.Series:
    """
    Convert a dictionary of portfolio weights into a pandas Series
    aligned with the asset columns of the returns DataFrame.
    """
    weights_series = pd.Series(weights, dtype=float)

    weights_series = weights_series.reindex(asset_names)

    if weights_series.isna().any():
        missing_assets = weights_series[weights_series.isna()].index.tolist()
        raise ValueError(f"Missing weights for assets: {missing_assets}")

    return weights_series


def validate_weights(
    weights: pd.Series,
    tolerance: float = 1e-6,
) -> None:
    """
    Validate that portfolio weights sum to 1 and are not negative.
    """
    total_weight = weights.sum()

    if not np.isclose(total_weight, 1.0, atol=tolerance):
        raise ValueError(f"Portfolio weights must sum to 1. Current sum: {total_weight}")

    if (weights < 0).any():
        negative_assets = weights[weights < 0].index.tolist()
        raise ValueError(f"Portfolio weights cannot be negative: {negative_assets}")


def compute_portfolio_returns(
    returns: pd.DataFrame,
    weights: dict[str, float] | pd.Series,
) -> pd.Series:
    """
    Compute daily portfolio returns from asset returns and portfolio weights.

    Portfolio return at each date is the weighted sum of asset returns.
    """
    if isinstance(weights, dict):
        weights = weights_to_series(weights, returns.columns.tolist())

    weights = weights.reindex(returns.columns)
    validate_weights(weights)

    portfolio_returns = returns.dot(weights)

    return portfolio_returns


def compute_multiple_portfolio_returns(
    returns: pd.DataFrame,
    portfolios: dict[str, dict[str, float]] = DEFAULT_PORTFOLIOS,
) -> pd.DataFrame:
    """
    Compute daily returns for multiple portfolios.
    """
    portfolio_returns = pd.DataFrame(index=returns.index)

    for portfolio_name, weights in portfolios.items():
        portfolio_returns[portfolio_name] = compute_portfolio_returns(
            returns=returns,
            weights=weights,
        )

    return portfolio_returns


def compute_portfolio_cumulative_returns(
    portfolio_returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute cumulative returns for portfolio returns.
    """
    cumulative_returns = (1 + portfolio_returns).cumprod()

    return cumulative_returns


def compute_portfolio_cagr(
    portfolio_returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """
    Compute CAGR for each portfolio from daily portfolio returns.
    """
    cumulative_returns = compute_portfolio_cumulative_returns(portfolio_returns)

    total_growth = cumulative_returns.iloc[-1]

    number_of_years = len(portfolio_returns) / trading_days

    cagr = total_growth ** (1 / number_of_years) - 1

    return cagr


def compute_portfolio_summary(
    portfolio_returns: pd.DataFrame,
    risk_free_rate: float = RISK_FREE_RATE,
) -> pd.DataFrame:
    """
    Compute a summary table with risk and return metrics for portfolios.
    """
    summary = pd.DataFrame(
        {
            "Annualized Return": compute_annualized_return(portfolio_returns),
            "CAGR": compute_portfolio_cagr(portfolio_returns),
            "Annualized Volatility": compute_annualized_volatility(portfolio_returns),
            "Maximum Drawdown": compute_max_drawdown(portfolio_returns),
            "Sharpe Ratio": compute_sharpe_ratio(
                portfolio_returns,
                risk_free_rate=risk_free_rate,
            ),
            "Sortino Ratio": compute_sortino_ratio(
                portfolio_returns,
                risk_free_rate=risk_free_rate,
            ),
            "Historical VaR 95%": compute_historical_var(
                portfolio_returns,
                confidence_level=0.95,
            ),
            "Historical CVaR 95%": compute_historical_cvar(
                portfolio_returns,
                confidence_level=0.95,
            ),
        }
    )

    return summary


def save_portfolio_returns(
    portfolio_returns: pd.DataFrame,
    filename: str = "portfolio_returns.csv",
) -> None:
    """
    Save portfolio returns to CSV.
    """
    output_path = PROCESSED_DATA_DIR / filename
    portfolio_returns.to_csv(output_path)

    print(f"Portfolio returns saved to: {output_path}")


def save_portfolio_summary(
    portfolio_summary: pd.DataFrame,
    filename: str = "portfolio_summary.csv",
) -> None:
    """
    Save portfolio summary to CSV.
    """
    output_path = PROCESSED_DATA_DIR / filename
    portfolio_summary.to_csv(output_path)

    print(f"Portfolio summary saved to: {output_path}")


def main() -> None:
    returns = load_returns()

    portfolio_returns = compute_multiple_portfolio_returns(returns)
    portfolio_summary = compute_portfolio_summary(portfolio_returns)

    save_portfolio_returns(portfolio_returns)
    save_portfolio_summary(portfolio_summary)


if __name__ == "__main__":
    main()