import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf


def examine_rainfall():
    df = pd.read_csv('HKO-Weather-Data-Interpolated.csv', usecols=['Date', 'TotalRainfall'])
    dates = pd.to_datetime(df['Date'])
    y = df['TotalRainfall']
    # plot against time
    plt.title('Daily Rainfall from 2000 to 2023')
    plt.plot(dates, y)
    plt.savefig('figs/daily_rainfall_raw.png')
    plt.clf()
    # differenced series plotted against time
    y_diff = y.diff()[1:]
    plt.title('Plot of differenced daily rainfall series')
    plt.plot(dates[1:], y_diff)
    plt.savefig('figs/daily_rainfall_differenced.png')
    plt.clf()
    # plot the autocorrelation function (acf)
    plot_acf(y_diff, lags=40, auto_ylims=True)
    plt.savefig('figs/daily_rainfall_differenced_acf.png')

if __name__ == '__main__':
    examine_rainfall()