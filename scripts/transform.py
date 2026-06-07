import pandas as pd
import numpy as np

def transform_stock_data(filepath):
    print("Loading raw data...")
    df = pd.read_csv(filepath, header=[0, 1], index_col=0)
    

    df.columns = ['_'.join(col).strip() for col in df.columns]
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    
    print("Transforming data...")
    

    stocks = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']
    
    transformed_dfs = []
    
    for stock in stocks:
        close_col = f'Close_{stock}'
        volume_col = f'Volume_{stock}'
        
        temp_df = pd.DataFrame()
        temp_df['date'] = pd.to_datetime(df.index)
        temp_df['stock'] = stock
        temp_df['close_price'] = df[close_col].values
        temp_df['volume'] = df[volume_col].values
        

        temp_df['daily_return'] = temp_df['close_price'].pct_change() * 100
        

        temp_df['7day_ma'] = temp_df['close_price'].rolling(window=7).mean()
        

        temp_df['30day_ma'] = temp_df['close_price'].rolling(window=30).mean()
        

        temp_df['volatility'] = temp_df['daily_return'].rolling(window=7).std()
        
        transformed_dfs.append(temp_df)
    

    final_df = pd.concat(transformed_dfs, ignore_index=True)
    final_df = final_df.dropna()
    
    print(f"Transformation complete! Shape: {final_df.shape}")
    print(f"\nSample of transformed data:")
    print(final_df.head(10))
    
    return final_df


df_transformed = transform_stock_data('../data/raw_stock_data.csv')


df_transformed.to_csv('C:/Users/vhuga/Desktop/SIDE PROJECTS/finance-data-pipeline/data/transformed_stock_data.csv', index=False)
print("\nTransformed data saved to data/transformed_stock_data.csv")