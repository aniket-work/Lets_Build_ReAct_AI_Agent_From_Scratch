import yfinance as yf


def calculate_financial_ratio(args):
    ticker, ratio = args.split(', ')
    stock = yf.Ticker(ticker)

    if ratio == 'P/E':
        value = stock.info['trailingPE']
    elif ratio == 'P/B':
        value = stock.info['priceToBook']
    elif ratio == 'D/E':
        value = stock.info['debtToEquity']
    else:
        return f"Ratio {ratio} not supported"

    return f"The {ratio} ratio for {ticker} is {value:.2f}"


def calculate_industry_average(industry, ratio):
    # This is a placeholder function. In a real-world scenario,
    # you would fetch this data from a financial data provider.
    industry_averages = {
        'SOFTWARE': {'P/E': 25.2, 'P/B': 3.8, 'D/E': 0.5},
        'HARDWARE': {'P/E': 22.1, 'P/B': 3.2, 'D/E': 0.4},
    }
    return industry_averages.get(industry, {}).get(ratio, "Data not available")