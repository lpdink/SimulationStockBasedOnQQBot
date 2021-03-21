import tushare as ts


def getCurrentQuote(id):
    df = ts.get_realtime_quotes('000581')  # Single stock symbol
    return df

def getCurrentPrice(id):
    return float(getCurrentQuote(id)['price'][0])