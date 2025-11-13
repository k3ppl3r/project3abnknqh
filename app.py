from flask import Flask, render_template, request
import pandas as pd
import requests
import pygal

app = Flask(__name__)

API_KEY = "UR1PMT0J4A3CQ60H"

#pull stock data
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" not in data:
        return None
    time_series = data["Time Series (Daily)"]
    dates = []
    prices = []
    for date, values in sorted(time_series.items()):
        dates.append(date)
        prices.append(float(values["4. close"]))
    return dates, prices

@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.read_csv("stocks.csv")
    stock_symbols = df["Symbol"].tolist()

    chart = None
    selected_symbol = None

#post
    if request.method == 'POST':
        selected_symbol = request.form['symbol']
        result = get_stock_data(selected_symbol)
        if result:
            dates, prices = result
            chart = pygal.Line(x_label_rotation=45)
            chart.title = f"{selected_symbol} Closing Prices"
            chart.x_labels = dates[-30:]
            chart.add('Close', prices[-30:])
            chart.render_to_file('static/chart.svg')

    return render_template('index.html', stock_symbols=stock_symbols, selected_symbol=selected_symbol, chart=chart)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)