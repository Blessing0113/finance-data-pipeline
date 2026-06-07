import pandas as pd
from sqlalchemy import Date
from sqlalchemy import create_engine, text


import pyodbc

def create_database():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=VHUGALAT-RG;"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'FinanceDB') CREATE DATABASE FinanceDB")
    conn.close()
    print("FinanceDB created successfully!")


create_database()

def load_stock_data(filepath):
    print("Loading transformed data...")
    df = pd.read_csv(filepath)
    
  
    connection_string = (
        "mssql+pyodbc://VHUGALAT-RG/FinanceDB"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
    
    print("Connecting to SQL Server...")
    engine = create_engine(connection_string)
    
    df['date'] = pd.to_datetime(df['date'])

    df.to_sql(
    name='stock_prices',
    con=engine,
    if_exists='replace',
    index=False,
    schema='dbo',
    dtype={'date': Date()}  
        )
    
    print(f"Data loaded successfully! {len(df)} rows inserted into stock_prices table")
    

    print("\nVerifying data in SQL Server...")
    
    with engine.connect() as conn:
        
        result = conn.execute(text("SELECT COUNT(*) as total_rows FROM dbo.stock_prices"))
        print(f"Total rows in database: {result.fetchone()[0]}")
        

        result = conn.execute(text("SELECT DISTINCT stock FROM dbo.stock_prices"))
        stocks = [row[0] for row in result.fetchall()]
        print(f"Stocks in database: {stocks}")
        

        result = conn.execute(text("""
            SELECT 
                stock,
                ROUND(AVG(close_price), 2) as avg_price,
                ROUND(AVG(daily_return), 4) as avg_daily_return,
                ROUND(AVG(volatility), 4) as avg_volatility
            FROM dbo.stock_prices
            GROUP BY stock
            ORDER BY avg_price DESC
        """))
        
        print("\nStock Summary from SQL Server:")
        print(f"{'Stock':<10} {'Avg Price':>12} {'Avg Return':>12} {'Avg Volatility':>15}")
        print("-" * 52)
        for row in result.fetchall():
            print(f"{row[0]:<10} ${row[1]:>11} {row[2]:>11}% {row[3]:>15}")
    
    return engine


engine = load_stock_data('../data/transformed_stock_data.csv')
print("\nETL Pipeline Complete! Data is now in SQL Server!")