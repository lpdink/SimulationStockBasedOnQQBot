import tushare as ts
import os
from datetime import date


def getCurrentQuote(id):
    df = ts.get_realtime_quotes('000581')  # Single stock symbol
    return df

def getCurrentPrice(id):
    return float(getCurrentQuote(id)['price'][0])

def saveTodayCSV():
    filename = '../csv/' + date.today().__str__() + '.csv'
    if os.path.exists(filename):
        return
    else:
        df = ts.get_today_all()
        df.to_csv(filename)