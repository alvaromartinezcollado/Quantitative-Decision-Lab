import numpy as np
import pandas as pd

from config import PROCESSED_DATA_DIR


TRADING_DAYS_PER_YEAR = 252
RISK_FREE_RATE = 0.02


def load_prices(
    filename: str = "adjusted_close_prices.csv",
) -> pd.DataFrame:
    """
    Load cleaned adjusted close prices.
    """
    path = PROCESSED_DATA_DIR / filename

    prices = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
    )

    return prices


def load_returns(
    filename: str = "simple_returns.csv",
) -> pd.DataFrame:
    """
    Load daily simple returns.
    """
    path = PROCESSED_DATA_DIR / filename

    returns = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
    )

    return returns


def compute_annualized_return(
    returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """
    Compute annualized arithmetic return from daily returns.
    """
    annualized_return = returns.mean() * trading_days

    return annualized_return


def compute_annualized_volatility(
    returns: pd.DataFrame,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """
    Compute annualized volatility from daily returns.
    """
    annualized_volatility = returns.std() * np.sqrt(trading_days)

    return annualized_volatility


def compute_cagr(
    prices: pd.DataFrame,
) -> pd.Series:
    """
    Compute Compound Annual Growth Rate.
    """
    start_prices = prices.iloc[0]
    end_prices = prices.iloc[-1]

    number_of_years = (prices.index[-1] - prices.index[0]).days / 365.25

    cagr = (end_prices / start_prices) ** (1 / number_of_years) - 1

    return cagr


def compute_cumulative_returns(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute cumulative returns from daily returns.
    """
    cumulative_returns = (1 + returns).cumprod()

    return cumulative_returns


def compute_drawdowns(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute drawdown series from daily returns.
    """
    cumulative_returns = compute_cumulative_returns(returns)
    running_max = cumulative_returns.cummax()

    drawdowns = cumulative_returns / running_max - 1

    return drawdowns


def compute_max_drawdown(
    returns: pd.DataFrame,
) -> pd.Series:
    """
    Compute maximum drawdown for each asset.
    """
    drawdowns = compute_drawdowns(returns)
    max_drawdown = drawdowns.min()

    return max_drawdown


def compute_cumulative_returns(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute cumulative returns from daily returns.
    """
    cumulative_returns = (1 + returns).cumprod()

    return cumulative_returns


def compute_drawdowns(
    returns: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compute drawdown series from daily returns.
    """
    cumulative_returns = compute_cumulative_returns(returns)
    running_max = cumulative_returns.cummax()

    drawdowns = cumulative_returns / running_max - 1

    return drawdowns

def compute_sharpe_ratio(
    returns: pd.DataFrame,
    risk_free_rate: float = RISK_FREE_RATE,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """
    Compute annualized Sharpe ratio.
    """
    annualized_return = compute_annualized_return(returns, trading_days)
    annualized_volatility = compute_annualized_volatility(returns, trading_days)

    excess_return = annualized_return - risk_free_rate

    sharpe_ratio = excess_return / annualized_volatility

    return sharpe_ratio


def compute_sortino_ratio(
    returns: pd.DataFrame,
    risk_free_rate: float = RISK_FREE_RATE,
    trading_days: int = TRADING_DAYS_PER_YEAR,
) -> pd.Series:
    """
    Compute annualized Sortino ratio.
    """
    annualized_return = compute_annualized_return(returns, trading_days)

    daily_risk_free_rate = risk_free_rate / trading_days

    downside_returns = returns.copy()
    downside_returns = downside_returns[downside_returns < daily_risk_free_rate]

    downside_deviation = downside_returns.std() * np.sqrt(trading_days)

    excess_return = annualized_return - risk_free_rate

    sortino_ratio = excess_return / downside_deviation

    return sortino_ratio


def compute_historical_var(
    returns: pd.DataFrame,
    confidence_level: float = 0.95,
) -> pd.Series:
    """
    Compute historical Value at Risk.

    For a 95% confidence level, VaR is the 5th percentile of returns.
    The result is returned as a positive loss number.
    """
    percentile = 1 - confidence_level

    var = returns.quantile(percentile)

    return -var


def compute_historical_cvar(
    returns: pd.DataFrame,
    confidence_level: float = 0.95,
) -> pd.Series:
    """
    Compute historical Conditional Value at Risk.

    CVaR is the average loss beyond the VaR threshold.
    The result is returned as a positive loss number.
    """
    var_threshold = returns.quantile(1 - confidence_level)

    cvar = returns[returns.le(var_threshold)].mean()

    return -cvar


def build_risk_summary(
    prices: pd.DataFrame,
    returns: pd.DataFrame,
    risk_free_rate: float = RISK_FREE_RATE,
) -> pd.DataFrame:
    """
    Build a summary table with main risk and return metrics.
    """
    summary = pd.DataFrame(
        {
            "Annualized Return": compute_annualized_return(returns),
            "CAGR": compute_cagr(prices),
            "Annualized Volatility": compute_annualized_volatility(returns),
            "Maximum Drawdown": compute_max_drawdown(returns),
            "Sharpe Ratio": compute_sharpe_ratio(
                returns,
                risk_free_rate=risk_free_rate,
            ),
            "Sortino Ratio": compute_sortino_ratio(
                returns,
                risk_free_rate=risk_free_rate,
            ),
            "Historical VaR 95%": compute_historical_var(
                returns,
                confidence_level=0.95,
            ),
            "Historical CVaR 95%": compute_historical_cvar(
                returns,
                confidence_level=0.95,
            ),
        }
    )

    return summary


def save_risk_summary(
    summary: pd.DataFrame,
    filename: str = "risk_summary.csv",
) -> None:
    """
    Save risk summary table.
    """
    output_path = PROCESSED_DATA_DIR / filename
    summary.to_csv(output_path)

    print(f"Risk summary saved to: {output_path}")


def main() -> None:
    prices = load_prices()
    returns = load_returns()

    summary = build_risk_summary(prices, returns)

    save_risk_summary(summary)


if __name__ == "__main__":
    main()