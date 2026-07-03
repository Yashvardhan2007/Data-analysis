[IF YOU WANT TO SEE A VISUAL CHART GO TO THE NOTEBOOK FOLDER -> CHARTS]


# Quantitative Analysis: Hyperliquid Trader Performance vs. Market Sentiment
[A Production-Grade Web3 Behavioral Data Science Case Study]

This repository contains a full-scale quantitative analysis exploring the statistical relationships between active trader execution performance (on Hyperliquid) and macroeconomic sentiment regimes (Bitcoin Fear & Greed Index). 

Processing **184,263 core trading observations**, this project moves past basic descriptive statistics to leverage hypothesis testing, cohort stratification, and risk-metric modeling to uncover actionable trading alphas.

---

##  Core Insights & Behavioral Discoveries

### 1. Statistical Invalidation of the Null Hypothesis
* **T-Statistic:** `-5.8046` | **P-Value:** `6.4896e-09`
* **Finding:** The relationship between macroeconomic sentiment classification and individual trader profitability is **statistically highly significant**. The variance in returns across market states is completely independent of random noise, proving sentiment data acts as a valid feature for systematic trading algorithms.

### 2. The Extreme Greed Leverage Trap
* **The Phenomenon:** When the market shifts to **Extreme Greed**, professional traders (**Alpha Masters**) face severe underperformance—their average PnL drops to a mere **$0.82** and win rate plummets to **21.27%**. 
* **The Root Cause:** The data highlights a sharp psychological trap: Alpha accounts violently scale up their exposure to a massive **32.11x average leverage** trying to fight the trend or perfectly top-tick the market, leading to rapid stop-outs. 
* Contrastingly, retail momentum buyers (**Retail Trapped**) maintain high win rates (**72.12%**) buying the local continuation, though capture limited absolute value (**$45.90 average PnL**).

### 3. Directional Shorting Alpha ($143.61 Avg PnL)
* **Finding:** Counter-intuitively, during standard **Greed** regimes, **SELL (Short) positions overwhelmingly outperform BUY (Long) positions**, netting an average of **$143.61** vs **$12.49** per trade. This shows that fading local structural extensions on Hyperliquid during bullish regimes yields massive historical risk-adjusted returns.

---

##  Performance Matrix: Cohort & Risk Stratification

| Trader Cohort | Sentiment Regime | Average PnL (USD) | Average Leverage Used | Win Rate (%) |
| :--- | :--- | :---: | :---: | :---: |
| **Alpha Masters** | Greed | **$173.04** | 4.58x | **51.45%** |
| **Alpha Masters** | Neutral | $110.02 | 7.95x | 30.76% |
| **Alpha Masters** | Fear | $68.44 | 4.88x | 42.19% |
| **Alpha Masters** | Extreme Greed | $0.82 | **32.11x** | 21.27% |
| **Retail Trapped** | Extreme Greed | $45.91 | 9.36x | **72.12%** |
| **Retail Trapped** | Greed | $37.74 | 10.12x | 40.64% |
| **Retail Trapped** | Fear | $30.04 | 12.28x | 40.78% |
| **Retail Trapped** | Neutral | -$9.41 | 13.52x | 32.06% |

