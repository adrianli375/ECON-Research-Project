from datetime import datetime
import pandas as pd
import re
from tqdm import tqdm


WEATHER_DF = pd.read_csv('HKO-Weather-Data-Interpolated.csv', usecols=['Date', 'TotalRainfall'])
LATEST_DATA_START_DATES = [datetime(2023, 7, 15), datetime(2023, 7, 26), datetime(2023, 8, 30),
                           datetime(2023, 9, 4), datetime(2023, 10, 4)]
LATEST_DATA_END_DATES = [datetime(2023, 7, 18), datetime(2023, 7, 28), datetime(2023, 9, 2),
                         datetime(2023, 9, 5), datetime(2023, 10, 9)]
LATEST_DATA_TIMEDELTA = [datetime(2023, 7, 18, 8, 40) - datetime(2023, 7, 15, 4, 40),
                         datetime(2023, 7, 28, 12, 40) - datetime(2023, 7, 26, 20, 40),
                         datetime(2023, 9, 2, 23, 40) - datetime(2023, 8, 30, 17, 40),
                         datetime(2023, 9, 5, 21, 40) - datetime(2023, 9, 4, 4, 40),
                         datetime(2023, 10, 9, 16, 20) - datetime(2023, 10, 4, 21, 40)]
LATEST_DATA_MAX_SIGNAL = ['8', '1', '10', '1', '9']


def main():
    df = pd.DataFrame(columns=['Year', 'Month', 'StartDate', 'EndDate', 'DaysInEffect', 'MinsInEffect', 
                               'ClosestDistance', 'MaxSignal', 'TotalRainfall'])
    raw_df = pd.read_excel('raw-data/TC_Impact_Data_HKO.xlsx', sheet_name='Signal Data',
                           skiprows=1).iloc[3:]
    raw_df = raw_df[raw_df['Year'] >= 2000].reset_index(drop=True)
    for i in tqdm(range(len(raw_df))):
        start_date = raw_df.at[i, 'Issuance Date of First \nTC Warning Signal\nDuring this Passage'].to_pydatetime()
        end_date = raw_df.at[i, 'Cancellation Date of all \nTC Warning Signal \nDuring this Passage'].to_pydatetime()
        year, month = start_date.year, start_date.month
        days_in_effect = (end_date - start_date).days + 1
        duration_raw = raw_df.at[i, 'Duration of all Issued TC Warning Signals During this Passage\n(hh:mm)']
        _match = re.search(r'(\d{1,2}):([0-5]\d)', duration_raw)
        hh, mm = int(_match.group(1)), int(_match.group(2))
        mins_in_effect = hh * 60 + mm
        closest_distance = raw_df.at[i, 'Closest Distance to \nHK (km)']
        max_signal = str(int(raw_df.at[i, 'Highest TC Warning \nSignal Issued\nDuring this Passage']))
        total_rainfall = get_total_rainfall(start_date, end_date)
        data_row = [year, month, start_date, end_date, days_in_effect, mins_in_effect, 
                    closest_distance, max_signal, total_rainfall]
        idx = len(df)
        df.loc[idx] = data_row
    # add latest data for 2023
    for i in range(len(LATEST_DATA_START_DATES)):
        start_date, end_date = LATEST_DATA_START_DATES[i], LATEST_DATA_END_DATES[i]
        year, month = start_date.year, start_date.month
        days_in_effect = (end_date - start_date).days + 1
        _timedelta = LATEST_DATA_TIMEDELTA[i]
        mins_in_effect = int(_timedelta.days * 24 * 60 + _timedelta.seconds / 60)
        closest_distance = None
        max_signal = LATEST_DATA_MAX_SIGNAL[i]
        total_rainfall = get_total_rainfall(start_date, end_date)
        data_row = [year, month, start_date, end_date, days_in_effect, mins_in_effect, 
                    closest_distance, max_signal, total_rainfall]
        idx = len(df)
        df.loc[idx] = data_row
    df.to_csv('HKO-Typhoon-History.csv', index=False)


def get_total_rainfall(start_date: datetime, end_date: datetime) -> float:
    sub_df = WEATHER_DF[(WEATHER_DF['Date'] >= start_date.strftime('%Y-%m-%d')) & 
                        (WEATHER_DF['Date'] <= end_date.strftime('%Y-%m-%d'))]
    total_rainfall = sub_df['TotalRainfall'].sum()
    return total_rainfall


if __name__ == '__main__':
    main()
