import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from sqlalchemy import create_engine, text


engine = create_engine('sqlite:///../data/finance.db')


df = pd.read_csv('../data/transformed_stock_data.csv')
df['date'] = pd.to_datetime(df['date'])


sns.set_theme(style="darkgrid")
colors = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0', '#FF9800']
stocks = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']


fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Stock Market Analysis Dashboard\n2024 - 2025', 
             fontsize=18, fontweight='bold', y=1.02)


ax1 = axes[0, 0]
for i, stock in enumerate(stocks):
    stock_df = df[df['stock'] == stock]
    ax1.plot(stock_df['date'], stock_df['close_price'], 
             label=stock, color=colors[i], linewidth=1.5)
ax1.set_title('Stock Price Over Time', fontweight='bold')
ax1.set_ylabel('Price (USD)')
ax1.legend(loc='upper left')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)


ax2 = axes[0, 1]
for i, stock in enumerate(stocks):
    stock_df = df[df['stock'] == stock]
    ax2.plot(stock_df['date'], stock_df['30day_ma'],
             label=stock, color=colors[i], linewidth=1.5)
ax2.set_title('30-Day Moving Average (Trend)', fontweight='bold')
ax2.set_ylabel('Price (USD)')
ax2.legend(loc='upper left')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)


ax3 = axes[1, 0]
volatility_data = df.groupby('stock')['volatility'].mean().sort_values(ascending=False)
bars = ax3.bar(volatility_data.index, volatility_data.values, color=colors)
ax3.set_title('Average Volatility by Stock (Risk)', fontweight='bold')
ax3.set_ylabel('Volatility (%)')
for bar, val in zip(bars, volatility_data.values):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{val:.2f}%', ha='center', va='bottom', fontweight='bold')


ax4 = axes[1, 1]
for i, stock in enumerate(stocks):
    stock_df = df[df['stock'] == stock].copy()
    stock_df = stock_df.sort_values('date')
    stock_df['cumulative_return'] = (1 + stock_df['daily_return'] / 100).cumprod() - 1
    ax4.plot(stock_df['date'], stock_df['cumulative_return'] * 100,
             label=stock, color=colors[i], linewidth=1.5)
ax4.set_title('Cumulative Returns (%)', fontweight='bold')
ax4.set_ylabel('Return (%)')
ax4.axhline(y=0, color='white', linestyle='--', alpha=0.5)
ax4.legend(loc='upper left')
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax4.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()


plt.savefig('../dashboard/stock_dashboard.png', dpi=150, bbox_inches='tight')
print("Dashboard saved to dashboard/stock_dashboard.png")
plt.show()
print("Visualization complete!")