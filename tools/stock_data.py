import yfinance as yf


def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    current_price = stock.info['currentPrice']
    return f"The current stock price of {ticker} is ${current_price:.2f}"


def calculate_moving_average(args):
    ticker, days = args.split(', ')
    stock = yf.Ticker(ticker)
    hist = stock.history(period=f"{days}d")
    ma = hist['Close'].mean()
    return f"The {days}-day moving average for {ticker} is ${ma:.2f}"