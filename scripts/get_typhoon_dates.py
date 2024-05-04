# --- this script gets the date of typhoons
# --- whenever there is any typhoon signal hoisted (no. 1 or above)

from datetime import datetime, timedelta
import pandas as pd

LATEST_TYPHOON_DATES = [
    datetime(2023, 7, 15),
    datetime(2023, 7, 16),
    datetime(2023, 7, 17),
    datetime(2023, 7, 18),
    datetime(2023, 7, 26),
    datetime(2023, 7, 27),
    datetime(2023, 7, 28),
    datetime(2023, 8, 30),
    datetime(2023, 8, 31),
    datetime(2023, 9, 1),
    datetime(2023, 9, 2),
    datetime(2023, 9, 4),
    datetime(2023, 9, 5),
    datetime(2023, 10, 4),
    datetime(2023, 10, 5),
    datetime(2023, 10, 6),
    datetime(2023, 10, 7),
    datetime(2023, 10, 8),
    datetime(2023, 10, 9)
]


def get_typhoon_date_list(): 
    typhoon_dates = []
    raw_df = pd.read_excel('raw-data/TC_Impact_Data_HKO.xlsx', sheet_name='Signal Data',
                           skiprows=1).iloc[3:]
    raw_df = raw_df[raw_df['Year'] >= 2000].reset_index(drop=True)
    for i in range(len(raw_df)):
        start_date = raw_df.at[i, 'Issuance Date of First \nTC Warning Signal\nDuring this Passage'].to_pydatetime()
        end_date = raw_df.at[i, 'Cancellation Date of all \nTC Warning Signal \nDuring this Passage'].to_pydatetime()
        curr_date = start_date
        while curr_date <= end_date:
            typhoon_dates.append(curr_date)
            curr_date += timedelta(days=1)
    typhoon_dates.extend(LATEST_TYPHOON_DATES)
    return sorted(list(set(typhoon_dates)))

