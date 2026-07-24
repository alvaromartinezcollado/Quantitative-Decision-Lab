import numpy as np
import pandas as pd

from config import PROCESSED_DATA_DIR
from risk_metrics import load_returns
from portfolio import (
    DEFAULT_PORTFOLIOS,
    weights_to_series,
    validate_weights,
)


DEFAULT_SCENARIOS = {
    "Market Crash": {
        "AAPL": -0.25,
        "MSFT": -0.25,
        "NVDA": -0.35,
        "JPM": -0.30,
        "XOM": -0.20,
        "SPY": -0.25,
        "TLT": 0.08,
        "GLD": 0.10,
    },
    "Tech Selloff": {
        "AAPL": -0.25,
        "MSFT": -0.25,
        "NVDA": -0.40,
        "JPM": -0.10,
        "XOM": -0.05,
        "SPY": -0.15,
        "TLT": 0.03,
        "GLD": 0.05,
    },
    "Interest Rate Shock": {
        "AAPL": -0.12,
        "MSFT": -0.12,
        "NVDA": -0.20,
        "JPM": 0.05,
        "XOM": 0.02,
        "SPY": -0.10,
        "TLT": -0.18,
        "GLD": -0.05,
    },
    "Energy Shock": {
        "AAPL": -0.08,
        "MSFT": -0.08,
        "NVDA": -0.12,
        "JPM": -0.05,
        "XOM": 0.20,
        "SPY": -0.08,
        "TLT": 0.02,
        "GLD": 0.08,
    },
    "Inflation Shock": {
        "AAPL": -0.15,
        "MSFT": -0.15,
        "NVDA": -0.25,
        "JPM": -0.05,
        "XOM": 0.15,
        "SPY": -0.12,
        "TLT": -0.20,
        "GLD": 0.12,
    },
    "Risk-Off Scenario": {
        "AAPL": -0.18,
        "MSFT": -0.18,
        "NVDA": -0.30,
        "JPM": -0.20,
        "XOM": -0.15,
        "SPY": -0.18,
        "TLT": 0.10,
        "GLD": 0.12,
    },
}


def shocks_to_series(
    shocks: dict[str, float],
    asset_names: list[str],
) -> pd.Series:
    """
    Convert a dictionary of scenario shocks into a pandas Series
    aligned with the asset columns.
    """
    shocks_series = pd.Series(shocks, dtype=float)
    shocks_series = shocks_series.reindex(asset_names)

    if shocks_series.isna().any():
        missing_assets = shocks_series[shocks_series.isna()].index.tolist()
        raise ValueError(f"Missing shocks for assets: {missing_assets}")

    return shocks_series


def compute_portfolio_scenario_impact(
    weights: dict[str, float] | pd.Series,
    shocks: dict[str, float] | pd.Series,
    asset_names: list[str],
) -> float:
    """
    Compute the impact of one scenario on one portfolio.

    Scenario impact is the weighted sum of asset shocks.
    """
    if isinstance(weights, dict):
        weights = weights_to_series(weights, asset_names)

    if isinstance(shocks, dict):
        shocks = shocks_to_series(shocks, asset_names)

    weights = weights.reindex(asset_names)
    shocks = shocks.reindex(asset_names)

    validate_weights(weights)

    scenario_impact = float(weights.dot(shocks))

    return scenario_impact


def compute_scenario_impact_matrix(
    portfolios: dict[str, dict[str, float]],
    scenarios: dict[str, dict[str, float]],
    asset_names: list[str],
) -> pd.DataFrame:
    """
    Compute scenario impacts for all portfolios and all scenarios.

    Rows are scenarios.
    Columns are portfolios.
    Values are portfolio returns under each scenario.
    """
    impact_matrix = pd.DataFrame(
        index=scenarios.keys(),
        columns=portfolios.keys(),
        dtype=float,
    )

    for scenario_name, shocks in scenarios.items():
        for portfolio_name, weights in portfolios.items():
            impact_matrix.loc[scenario_name, portfolio_name] = (
                compute_portfolio_scenario_impact(
                    weights=weights,
                    shocks=shocks,
                    asset_names=asset_names,
                )
            )

    return impact_matrix


def compute_scenario_contributions(
    weights: dict[str, float] | pd.Series,
    shocks: dict[str, float] | pd.Series,
    asset_names: list[str],
) -> pd.Series:
    """
    Compute asset-level contribution to portfolio scenario impact.

    Contribution of each asset = asset weight * asset shock.
    """
    if isinstance(weights, dict):
        weights = weights_to_series(weights, asset_names)

    if isinstance(shocks, dict):
        shocks = shocks_to_series(shocks, asset_names)

    weights = weights.reindex(asset_names)
    shocks = shocks.reindex(asset_names)

    validate_weights(weights)

    contributions = weights * shocks

    return contributions


def compute_all_scenario_contributions(
    portfolios: dict[str, dict[str, float]],
    scenarios: dict[str, dict[str, float]],
    asset_names: list[str],
) -> pd.DataFrame:
    """
    Compute asset-level scenario contributions for all portfolios and scenarios.

    The output has a MultiIndex:
    - Scenario
    - Portfolio

    Columns are assets.
    """
    rows = []

    for scenario_name, shocks in scenarios.items():
        for portfolio_name, weights in portfolios.items():
            contributions = compute_scenario_contributions(
                weights=weights,
                shocks=shocks,
                asset_names=asset_names,
            )

            contributions.name = (scenario_name, portfolio_name)
            rows.append(contributions)

    contributions_df = pd.DataFrame(rows)
    contributions_df.index = pd.MultiIndex.from_tuples(
        contributions_df.index,
        names=["Scenario", "Portfolio"],
    )

    return contributions_df


def compute_worst_scenario_by_portfolio(
    impact_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identify the worst scenario for each portfolio.
    """
    worst_scenario = impact_matrix.idxmin(axis=0)
    worst_impact = impact_matrix.min(axis=0)

    summary = pd.DataFrame(
        {
            "Worst Scenario": worst_scenario,
            "Worst Scenario Impact": worst_impact,
        }
    )

    return summary


def compute_best_scenario_by_portfolio(
    impact_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identify the best scenario for each portfolio.
    """
    best_scenario = impact_matrix.idxmax(axis=0)
    best_impact = impact_matrix.max(axis=0)

    summary = pd.DataFrame(
        {
            "Best Scenario": best_scenario,
            "Best Scenario Impact": best_impact,
        }
    )

    return summary


def compute_worst_portfolio_by_scenario(
    impact_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identify the worst-performing portfolio in each scenario.
    """
    worst_portfolio = impact_matrix.idxmin(axis=1)
    worst_impact = impact_matrix.min(axis=1)

    summary = pd.DataFrame(
        {
            "Worst Portfolio": worst_portfolio,
            "Worst Impact": worst_impact,
        }
    )

    return summary


def compute_best_portfolio_by_scenario(
    impact_matrix: pd.DataFrame,
) -> pd.DataFrame:
    """
    Identify the best-performing portfolio in each scenario.
    """
    best_portfolio = impact_matrix.idxmax(axis=1)
    best_impact = impact_matrix.max(axis=1)

    summary = pd.DataFrame(
        {
            "Best Portfolio": best_portfolio,
            "Best Impact": best_impact,
        }
    )

    return summary


def save_scenario_impact(
    impact_matrix: pd.DataFrame,
    filename: str = "scenario_impact.csv",
) -> None:
    """
    Save scenario impact matrix.
    """
    output_path = PROCESSED_DATA_DIR / filename
    impact_matrix.to_csv(output_path)

    print(f"Scenario impact saved to: {output_path}")


def save_scenario_contributions(
    contributions: pd.DataFrame,
    filename: str = "scenario_contributions.csv",
) -> None:
    """
    Save scenario contribution table.
    """
    output_path = PROCESSED_DATA_DIR / filename
    contributions.to_csv(output_path)

    print(f"Scenario contributions saved to: {output_path}")


def main() -> None:
    returns = load_returns()
    asset_names = returns.columns.tolist()

    impact_matrix = compute_scenario_impact_matrix(
        portfolios=DEFAULT_PORTFOLIOS,
        scenarios=DEFAULT_SCENARIOS,
        asset_names=asset_names,
    )

    contributions = compute_all_scenario_contributions(
        portfolios=DEFAULT_PORTFOLIOS,
        scenarios=DEFAULT_SCENARIOS,
        asset_names=asset_names,
    )

    save_scenario_impact(impact_matrix)
    save_scenario_contributions(contributions)


if __name__ == "__main__":
    main()