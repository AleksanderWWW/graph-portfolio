import yfinance as yf
import pandas as pd

def fetch_components():
    # Get current S&P 500 components from Wikipedia
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_df = tables[0]
    return sp500_df['Symbol'].tolist()

def fetch_data(stocks):
    data_list = []  # List to collect DataFrames for all stocks

    for stock in stocks:
        try:
            # Download data for the stock
            data_single = yf.download(
                stock,
                start='2006-01-01',
                end='2021-01-01',
                interval='1d',
                auto_adjust=True  # Auto-adjusts OHLC for splits/dividends
            )

            if not data_single.empty:
                # Add stock name and reset index to include "Date" as a column
                data_single = data_single.reset_index()
                data_single['Stock'] = stock  # Add stock name as a column
                data_list.append(data_single)  # Append to the list
        except Exception as e:
            print(f"Failed to fetch data for {stock}: {str(e)}")

    # Combine all DataFrames into one
    if data_list:
        combined_df = pd.concat(data_list, ignore_index=True)
        return combined_df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data

# Fetch all components from Wikipedia list
stocks = fetch_components()

# Begin storing data by the remainder from division by 10 of the list
stocks_init = stocks[(len(stocks) - len(stocks)%10):len(stocks)]
data_full = fetch_data(stocks_init)

# Remove MultiIndex to melt the data
data_full.columns = data_full.columns.droplevel(1)
# Melt the data for all observations
data_full = pd.melt(data_full, id_vars=['Date', 'Stock'], value_vars=['Close', 'Open'])
# Drop artificial NaNs
data_full = data_full.dropna(how='any')

# Download the data in batches of 10 stocks, repeat all the steps from initial download

for num in range(1, int(len(stocks)/10 + 1)):
  stocks_batch = stocks[((num-1)*10):(num*10)]
  data_batch = fetch_data(stocks_batch)
  data_batch.columns = data_batch.columns.droplevel(1)
  data_batch = pd.melt(data_batch, id_vars=['Date', 'Stock'], value_vars=['Close', 'Open'])
  data_batch = data_batch.dropna(how='any')
  data_full = pd.concat([data_full, data_batch], ignore_index = True)

# Sort the output
data_full = data_full.sort_values('Stock')
data_full.to_csv('output.csv', index=False)