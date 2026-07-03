import pandas as pd
import os

# Define paths to your files (Update the filenames if they are different)
raw_data_dir = "data/raw"
files = os.listdir(raw_data_dir)
print("Files in data/raw:", files)

# Find the files (assuming one has 'historical' or 'trader' and one has 'fear' or 'sentiment')
historical_file = [f for f in files if 'histor' in f.lower() or 'trader' in f.lower()][0]
sentiment_file = [f for f in files if 'fear' in f.lower() or 'sentiment' in f.lower()][0]

print(f"\n--- Loading {historical_file} ---")
df_trader = pd.read_csv(os.path.join(raw_data_dir, historical_file))
print("Columns:", df_trader.columns.tolist())
print("\nFirst 3 rows:")
print(df_trader.head(3))

print(f"\n--- Loading {sentiment_file} ---")
df_sentiment = pd.read_csv(os.path.join(raw_data_dir, sentiment_file))
print("Columns:", df_sentiment.columns.tolist())
print("\nFirst 3 rows:")
print(df_sentiment.head(3))