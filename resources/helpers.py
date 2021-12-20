from datetime import datetime

import pandas as pd


def moving_average(arr, n=3):
    """Returns a sliding window (of width n) over data from the iterable"""
    numbers_series = pd.Series(arr)
    windows = numbers_series.rolling(n)
    moving_averages = windows.mean()

    moving_averages_list = moving_averages.tolist()
    final_list = moving_averages_list[n - 1:]
    return [round(i, 2) for i in final_list]


def convert_time(date):
    """Convert time to convenient format"""
    return datetime.strptime(str(date), '%Y-%m-%d').strftime('%d/%m/%Y')
