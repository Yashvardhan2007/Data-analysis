import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# Set professional plotting layout
sns.set_theme(style="whitegrid")
os.makedirs('notebooks/charts', exist_ok=True)

print("🚀 Starting Production-Grade Web3 Data Science Pipeline...")

# 1. PIPELINE INITIALIZATION & DATA INGESTION
raw_data_dir = "data/raw"
df_trader = pd.read_csv(os.path.join(raw_data_dir, 'historical_data.csv'))
df_sentiment = pd.read_csv(os.path.join(raw_data_dir, 'fear_greed_index.csv'))

# Clean dates & map indices
df_trader['Datetime'] = pd.to_datetime(df_trader['Timestamp'], unit='ms', errors='coerce')
if df_trader['Datetime'].isnull().all():
    df_trader['Datetime'] = pd.to_datetime(df_trader['Timestamp IST'], errors='coerce')

df_trader['date_key'] = df_trader['Datetime'].dt.strftime('%Y-%m-%d')
df_sentiment['date_key'] = pd.to_datetime(df_sentiment['date']).dt.strftime('%Y-%m-%d')

# Core merge
df = pd.merge(df_trader, df_sentiment, on='date_key', how='inner')

# Clean key target variables
df['Closed PnL'] = pd.to_numeric(df['Closed PnL'], errors='coerce').fillna(0)
df['Size USD'] = pd.to_numeric(df['Size USD'], errors='coerce').fillna(0)
df['is_win'] = df['Closed PnL'] > 0

# Derive implicit leverage dynamically (Size USD / Margin or Start Position proxy)
if 'Start Position' in df.columns:
    df['Start Position Abs'] = pd.to_numeric(df['Start Position'], errors='coerce').abs()
    df['Calculated_Leverage'] = np.where(df['Start Position Abs'] > 0, df['Size USD'] / df['Start Position Abs'], 1)
    # Clip extreme outlines for cleaner statistical variance
    df['Calculated_Leverage'] = np.clip(df['Calculated_Leverage'], 1, 50)
else:
    df['Calculated_Leverage'] = 1

print(f"Dataset successfully compiled: {len(df)} core trading observations mapped.")

# --- PATTERN 1: STATISTICAL SIGNIFICANCE TESTING (T-TEST) ---
print("\n=== [1] STATISTICAL VALIDATION (HYPOTHESIS TESTING) ===")
fear_pnl = df[df['classification'] == 'Fear']['Closed PnL']
greed_pnl = df[df['classification'] == 'Greed']['Closed PnL']

t_stat, p_val = stats.ttest_ind(fear_pnl, greed_pnl, equal_var=False)
print(f"T-Statistic: {t_stat:.4f}")
print(f"P-Value: {p_val:.6e}")
if p_val < 0.05:
    print("👉 RESULT: Statistically Significant! The difference in trading performance between Fear and Greed is NOT random.")
else:
    print("👉 RESULT: Not Statistically Significant. The variance could be random noise.")

# --- PATTERN 2: TRADER BEHAVIORAL SEGMENTATION (SMART MONEY VS RETAIL) ---
print("\n=== [2] BEHAVIORAL COHORT SEGMENTATION ===")
# Profile individual accounts by overall profitability
account_profiles = df.groupby('Account').agg(
    net_lifetime_pnl=('Closed PnL', 'sum'),
    trade_count=('Closed PnL', 'count')
).reset_index()

# Filter out low-volume accounts to avoid noise
active_accounts = account_profiles[account_profiles['trade_count'] >= 5]
p75 = active_accounts['net_lifetime_pnl'].quantile(0.75)

# Label accounts: "Alpha Masters" (top 25% profitable) vs "Retail Trapped"
df['trader_cohort'] = 'Retail Trapped'
alpha_accounts = active_accounts[active_accounts['net_lifetime_pnl'] >= p75]['Account']
df.loc[df['Account'].isin(alpha_accounts), 'trader_cohort'] = 'Alpha Masters'

cohort_analysis = df.groupby(['trader_cohort', 'classification']).agg(
    avg_pnl=('Closed PnL', 'mean'),
    avg_leverage=('Calculated_Leverage', 'mean'),
    win_rate=('is_win', 'mean')
).reset_index()
cohort_analysis['win_rate'] = (cohort_analysis['win_rate'] * 100).round(2)
print(cohort_analysis.to_string(index=False))

# --- PATTERN 3: STRATEGIC DIRECTIONAL BIAS ANALYSIS ---
print("\n=== [3] DIRECTIONAL BIAS ANALYSIS (SIDE vs SENTIMENT) ===")
if 'Side' in df.columns:
    side_sentiment = df.groupby(['classification', 'Side']).agg(
        avg_pnl=('Closed PnL', 'mean'),
        volume_count=('Closed PnL', 'count')
    ).reset_index()
    print(side_sentiment.to_string(index=False))

# --- GENERATE COMPREHENSIVE CHARTS ---
# Chart 1: Cohort Breakdown
plt.figure(figsize=(12, 6))
sns.barplot(data=cohort_analysis, x='classification', y='avg_pnl', hue='trader_cohort', palette='Set1')
plt.title('How Top Traders (Alphas) vs Retail Perform across Sentiment Regimes')
plt.ylabel('Average PnL (USD)')
plt.savefig('notebooks/charts/cohort_performance.png', bbox_inches='tight')
plt.close()

# Chart 2: PnL Volatility Boxplot (Tail Risk Analysis)
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='classification', y='Closed PnL', showfliers=False, palette='coolwarm')
plt.title('PnL Distribution and Margin Volatility Across Sentiments')
plt.savefig('notebooks/charts/pnl_distribution.png', bbox_inches='tight')
plt.close()

print("\n✓ Advanced insights framework executed successfully. Graphics exported to 'notebooks/charts/'")