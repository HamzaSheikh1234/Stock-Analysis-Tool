import yfinance as yf
import pandas as pd

def calculate_rolling_windows(ticker, start_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date)
    df['RollingMean'] = df['Close'].rolling(window=20).mean()
    df['RollingStd'] = df['Close'].rolling(window=20).std()
    company_name = stock.info['longName']
    return df, company_name

def calculate_bollinger_bands(ticker, start_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date)
    df['SMA'] = df['Close'].rolling(window=20).mean()
    df['UpperBand'] = df['SMA'] + (df['Close'].rolling(window=20).std() * 2)
    df['LowerBand'] = df['SMA'] - (df['Close'].rolling(window=20).std() * 2)
    company_name = stock.info['longName']
    return df, company_name

def calculate_fibonacci_levels(ticker, start_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date)
    max_price = df['Close'].max()
    min_price = df['Close'].min()
    diff = max_price - min_price
    levels = {
        'Level 1': max_price - 0.236 * diff,
        'Level 2': max_price - 0.382 * diff,
        'Level 3': max_price - 0.618 * diff
    }
    company_name = stock.info['longName']
    return levels, df, company_name

def calculate_pivot_points(ticker, start_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date)
    df['Pivot'] = (df['High'].shift(1) + df['Low'].shift(1) + df['Close'].shift(1)) / 3
    df['Support1'] = (2 * df['Pivot']) - df['High'].shift(1)
    df['Resistance1'] = (2 * df['Pivot']) - df['Low'].shift(1)
    df['Support2'] = df['Pivot'] - (df['High'].shift(1) - df['Low'].shift(1))
    df['Resistance2'] = df['Pivot'] + (df['High'].shift(1) - df['Low'].shift(1))
    company_name = stock.info['longName']
    return df['Pivot'][-1], df['Support1'][-1], df['Resistance1'][-1], df['Support2'][-1], df['Resistance2'][-1], df, company_name
