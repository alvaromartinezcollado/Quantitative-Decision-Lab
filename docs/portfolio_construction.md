# Portfolio Construction & Allocation

## Objective

The objective of this module is to move from individual asset analysis to portfolio-level analysis.

Instead of analysing each asset separately, this phase combines assets using different allocation weights in order to study how portfolio composition affects return, risk and diversification.

## Portfolio Concept

A portfolio is a combination of assets with assigned weights.

For example, a portfolio may allocate:

- 50% to equities;
- 30% to bonds;
- 20% to gold.

The portfolio return is the weighted sum of the returns of its individual assets.

## Portfolio Return Formula

For a portfolio with assets \(1, 2, ..., n\), the return at time \(t\) is:

\[
R_{p,t} = w_1 R_{1,t} + w_2 R_{2,t} + ... + w_n R_{n,t}
\]

where:

- \(R_{p,t}\) is the portfolio return at time \(t\);
- \(w_i\) is the weight of asset \(i\);
- \(R_{i,t}\) is the return of asset \(i\) at time \(t\).

## Portfolio Weights

Portfolio weights represent the percentage of capital allocated to each asset.

In this phase, all portfolios are long-only portfolios, meaning that:

- all weights are greater than or equal to zero;
- all weights sum to 1.

## Portfolios Analysed

The following portfolios are analysed:

### Equal Weight Portfolio

A simple benchmark portfolio where all assets have the same weight.

### Equity Heavy Portfolio

A portfolio with high exposure to equities and limited exposure to bonds and gold.

### Defensive Portfolio

A portfolio with higher exposure to bonds and gold, designed to reduce volatility and downside risk.

### Growth Tech Portfolio

A portfolio concentrated in technology and growth-oriented assets.

### Balanced Portfolio

A diversified portfolio combining equities, bonds and gold.

## Metrics Computed

For each portfolio, the following metrics are computed:

- Annualized Return;
- CAGR;
- Annualized Volatility;
- Maximum Drawdown;
- Sharpe Ratio;
- Sortino Ratio;
- Historical VaR 95%;
- Historical CVaR 95%.

## Interpretation

This module allows comparison between different allocation decisions.

A portfolio with high exposure to growth assets may achieve higher historical returns, but it may also suffer higher volatility and deeper drawdowns.

A more defensive portfolio may have lower historical returns, but can provide better stability and downside protection.

## Outputs

This module produces:

- daily returns for each portfolio;
- cumulative returns for each portfolio;
- portfolio-level risk and return summary;
- comparison tables and charts.

## Next Steps

The next phase will extend portfolio-level analysis and prepare the portfolios for scenario analysis and stress testing.