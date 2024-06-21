from flask import Flask, request, render_template
import indicators as ti
import earnings_analysis as ea
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)

def plot_to_img(fig):
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return base64.b64encode(output.getvalue()).decode('utf8')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ticker = request.form['ticker'].upper()
    start_date = request.form['start_date']
    analysis_type = request.form['analysis_type']
    
    if analysis_type == '1':
        df, company_name = ti.calculate_rolling_windows(ticker, start_date)
        fig, ax = plt.subplots()
        ax.plot(df['Close'], label='Close Price')
        ax.plot(df['RollingMean'], label='Rolling Mean', color='orange')
        ax.fill_between(df.index, df['RollingMean'] - df['RollingStd'], df['RollingMean'] + df['RollingStd'], color='gray', alpha=0.2)
        ax.set_title(f'{company_name} ({ticker}) Rolling Windows')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        img = plot_to_img(fig)
        return render_template('results.html', img=img)
    
    elif analysis_type == '2':
        df, company_name = ti.calculate_bollinger_bands(ticker, start_date)
        fig, ax = plt.subplots()
        ax.plot(df['Close'], label='Close Price', color='blue')
        ax.plot(df['SMA'], label='20-Day SMA', color='orange')
        ax.plot(df['UpperBand'], label='Upper Bollinger Band', color='green')
        ax.plot(df['LowerBand'], label='Lower Bollinger Band', color='red')
        ax.fill_between(df.index, df['UpperBand'], df['LowerBand'], color='grey', alpha=0.3)
        ax.set_title(f'{company_name} ({ticker}) Bollinger Bands')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        img = plot_to_img(fig)
        return render_template('results.html', img=img)
    
    elif analysis_type == '3':
        levels, df, company_name = ti.calculate_fibonacci_levels(ticker, start_date)
        fig, ax = plt.subplots()
        ax.plot(df['Close'], label='Close Price')
        for level, value in levels.items():
            ax.axhline(y=value, linestyle='--', alpha=0.5, label=f'Fibonacci {level} ({value:.2f})')
        ax.set_title(f'{company_name} ({ticker}) Fibonacci Retracement Levels')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        img = plot_to_img(fig)
        return render_template('results.html', img=img)
    
    elif analysis_type == '4':
        pivot, s1, r1, s2, r2, df, company_name = ti.calculate_pivot_points(ticker, start_date)
        fig, ax = plt.subplots()
        ax.plot(df['Close'], label='Close Price')
        ax.axhline(y=pivot, color='blue', linestyle='-', label=f'Pivot ({pivot:.2f})')
        ax.axhline(y=s1, color='green', linestyle='--', label=f'Support 1 ({s1:.2f})')
        ax.axhline(y=r1, color='red', linestyle='--', label=f'Resistance 1 ({r1:.2f})')
        ax.axhline(y=s2, color='green', linestyle='--', alpha=0.5, label=f'Support 2 ({s2:.2f})')
        ax.axhline(y=r2, color='red', linestyle='--', alpha=0.5, label=f'Resistance 2 ({r2:.2f})')
        ax.set_title(f'{company_name} ({ticker}) Pivot Points')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        img = plot_to_img(fig)
        return render_template('results.html', img=img)
    
    elif analysis_type == '5':
        output = ea.main(ticker, start_date)
        return render_template('results.html', output=output)
    
    else:
        return "Invalid choice."

if __name__ == "__main__":
    app.run(debug=True)
