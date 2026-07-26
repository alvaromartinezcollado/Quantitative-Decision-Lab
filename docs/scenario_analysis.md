# Scenario Analysis & Stress Testing

## Objective

The objective of this module is to evaluate how different portfolio allocations behave under hypothetical adverse market scenarios.

This phase moves the project from historical risk analysis to forward-looking decision analysis.

## Scenario Analysis

Scenario analysis studies how a portfolio would behave under a specific hypothetical situation.

Examples include:

- market crash;
- technology selloff;
- interest rate shock;
- energy shock;
- inflation shock;
- risk-off scenario.

## Stress Testing

Stress testing focuses on adverse or extreme scenarios.

The goal is not to predict exactly what will happen, but to understand portfolio vulnerabilities.

## Scenario Shock

A scenario shock is an assumed return for an asset under a given scenario.

For example:

- AAPL: -25%;
- NVDA: -40%;
- TLT: +5%;
- GLD: +8%.

## Portfolio Scenario Impact

The impact of a scenario on a portfolio is computed as:

Portfolio Scenario Impact = sum of asset weight × asset shock

For example, if a portfolio has 50% in SPY and 50% in GLD, and the scenario assumes SPY falls 20% while GLD rises 5%, then:

Portfolio Scenario Impact = 0.50 × (-20%) + 0.50 × 5% = -7.5%

## Scenarios Analysed

### Market Crash

A broad equity market crash where most stocks decline significantly, while defensive assets such as bonds and gold may rise.

### Tech Selloff

A scenario where technology and growth stocks fall sharply.

### Interest Rate Shock

A scenario where interest rates rise sharply, affecting long-duration bonds and growth stocks.

### Energy Shock

A scenario where energy prices move sharply, benefiting energy companies while pressuring other sectors.

### Inflation Shock

A scenario where inflation rises, pressuring bonds and growth stocks while potentially supporting energy and gold.

### Risk-Off Scenario

A scenario where investors reduce risk exposure, sell equities and move toward defensive assets.

## Outputs

This module produces:

- a scenario impact matrix;
- asset-level contribution analysis;
- worst scenario by portfolio;
- best scenario by portfolio;
- worst portfolio by scenario;
- best portfolio by scenario;
- average scenario impact;
- worst-case scenario impact.

## Interpretation

Scenario analysis helps identify vulnerabilities that may not appear clearly in historical risk metrics.

A portfolio may have strong historical returns but still be highly vulnerable to a technology selloff, interest rate shock or inflation shock.

## Limitations

The scenarios are hypothetical and depend on assumptions.

They are not predictions.

The analysis does not assign probabilities to scenarios.

The results depend heavily on the selected shocks.

Real market crises can behave differently from predefined scenarios.

Correlations between assets may change during stress periods.

## Next Steps

The next phase will use Monte Carlo simulation to generate many possible future outcomes instead of relying only on a small number of manually defined scenarios.