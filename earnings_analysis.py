import yfinance as yf
import pandas as pd

def get_earnings_dates(ticker):
    stock = yf.Ticker(ticker)
    earnings_dates = stock.earnings_dates.reset_index()
    earnings_dates.columns = ['Date', 'EPS']
    return earnings_dates

def calculate_earnings_analysis(ticker, start_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date)
    earnings_dates = get_earnings_dates(ticker)
    earnings_dates = earnings_dates[earnings_dates['Date'] > pd.to_datetime(start_date)]
    
    results = []
    for date in earnings_dates['Date']:
        try:
            date_str = date.strftime('%Y-%m-%d')
            before_date = df.index[df.index < date][[-1]][0]
            after_date = df.index[df.index > date][[0]][0]
            before = df.loc[before_date]['Close']
            after = df.loc[after_date]['Close']
            change = ((after - before) / before) * 100
            results.append((date_str, change))
        except Exception as e:
            print(f"Error processing date {date}: {e}")

    gains = [result[1] for result in results if result[1] > 0]
    losses = [result[1] for result in results if result[1] <= 0]
    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 0
    total_avg_change = sum([result[1] for result in results]) / len(results) if results else 0

    return {
        'results': results,
        'num_gains': len(gains),
        'num_losses': len(losses),
        'avg_gain': avg_gain,
        'avg_loss': avg_loss,
        'total_avg_change': total_avg_change,
    }

def main(ticker, start_date):
    analysis = calculate_earnings_analysis(ticker, start_date)
    results = analysis['results']
    output = f"Earnings Analysis for {ticker} since {start_date}:\n"
    for date, change in results:
        output += f"Date: {date}, Change: {change:.2f}%\n"
    output += f"Number of gains: {analysis['num_gains']}\n"
    output += f"Number of losses: {analysis['num_losses']}\n"
    output += f"Average gain: {analysis['avg_gain']:.2f}%\n"
    output += f"Average loss: {analysis['avg_loss']:.2f}%\n"
    output += f"Total average change: {analysis['total_avg_change']:.2f}%\n"
    return output
