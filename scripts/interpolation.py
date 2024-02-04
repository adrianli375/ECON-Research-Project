import pandas as pd


def interpolate():
    df = pd.read_csv('HKO-Weather-Data.csv')
    df_interpolated = df.interpolate()
    df_interpolated.to_csv('HKO-Weather-Data-Interpolated.csv', index=False)

if __name__ == '__main__':
    interpolate()
