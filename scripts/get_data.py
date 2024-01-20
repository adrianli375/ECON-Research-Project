from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm


from get_extreme_weather_dates import get_extreme_weather_date_list

START_DATE = datetime(2000, 1, 1)
END_DATE = datetime(2023, 11, 30)

MEAN_CLOUD_DF = pd.read_csv('raw-data/daily_HKO_CLD_ALL.csv', skiprows=2, skipfooter=4)
MEAN_PRESSURE_DF = pd.read_csv('raw-data/daily_TKL_MSLP_ALL.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
TOTAL_EVAPORATION_DF = pd.read_csv('raw-data/daily_KP_EVAP_ALL.csv', skiprows=2, skipfooter=4)
TOTAL_RAINFALL_DF = pd.read_csv('raw-data/daily_TKL_RF_ALL.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
MEAN_HUMIDITY_DF = pd.read_csv('raw-data/daily_TKL_RH_ALL.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
MIN_TEMPERATURE_DF = pd.read_csv('raw-data/CLMMINT_TKL_.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
MEAN_TEMPERATURE_DF = pd.read_csv('raw-data/CLMTEMP_TKL_.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
MAX_TEMPERATURE_DF = pd.read_csv('raw-data/CLMMAXT_TKL_.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
MEAN_UV_INDEX_DF = pd.read_csv('raw-data/daily_KP_UV_ALL.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
TOTAL_SUNSHINE_DF = pd.read_csv('raw-data/daily_KP_SUN_ALL.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
MEAN_WINDSPEED_DF = pd.read_csv('raw-data/daily_TKL_WSPD_ALL.csv', skiprows=2, skipfooter=4, encoding_errors='ignore')
EXTREME_DAYS = get_extreme_weather_date_list()

def get_value(df: pd.DataFrame, year: int, month: int, day: int):
    try:
        result_row = df[(df['年/Year'] == year) & 
                    (df['月/Month'] == month) & 
                    (df['日/Day'] == day)]['數值/Value']
        return_value = result_row.values.tolist()[0]
        if return_value == '***':
            return None
        return return_value
    except IndexError:
        return None

def main():
    df = pd.DataFrame(columns=['Year', 'Month', 'Day', 'Date', 'MeanCloudAmount', 'MeanPressure',
                               'TotalEvaporation', 'TotalRainfall', 'MeanHumidity', 
                               'MinTemperature', 'MeanTemperature', 'MaxTemperature', 
                               'MeanUVIndex', 'TotalSunshine', 'MeanWindSpeed', 'IsExtreme'])
    current_date = START_DATE
    pbar = tqdm(total=(END_DATE - START_DATE).days + 1)
    while current_date <= END_DATE:
        idx = len(df)
        current_year, current_month, current_day = current_date.year, current_date.month, current_date.day
        mean_cloud = get_value(MEAN_CLOUD_DF, current_year, current_month, current_day)
        mean_pressure = get_value(MEAN_PRESSURE_DF, current_year, current_month, current_day)
        total_evaporation = get_value(TOTAL_EVAPORATION_DF, current_year, current_month, current_day)
        total_rainfall = get_value(TOTAL_RAINFALL_DF, current_year, current_month, current_day)
        mean_humidity = get_value(MEAN_HUMIDITY_DF, current_year, current_month, current_day)
        min_temperature = get_value(MEAN_TEMPERATURE_DF, current_year, current_month, current_day)
        mean_temperature = get_value(MEAN_TEMPERATURE_DF, current_year, current_month, current_day)
        max_temperature = get_value(MAX_TEMPERATURE_DF, current_year, current_month, current_day)
        mean_uv_index = get_value(MEAN_UV_INDEX_DF, current_year, current_month, current_day)
        total_sunshine = get_value(TOTAL_SUNSHINE_DF, current_year, current_month, current_day)
        mean_windspeed = get_value(MEAN_WINDSPEED_DF, current_year, current_month, current_day)
        is_extreme = 1 if current_date in EXTREME_DAYS else 0
        data_row = [current_year, current_month, current_day, current_date, mean_cloud, 
                    mean_pressure, total_evaporation, total_rainfall, mean_humidity, min_temperature, 
                    mean_temperature, max_temperature, mean_uv_index, total_sunshine,
                    mean_windspeed, is_extreme]
        df.loc[idx] = data_row
        pbar.update(1)
        current_date += timedelta(days=1)
    pbar.close()
    df.to_csv('HKO-Weather-Data.csv', index=False)
    

if __name__ == '__main__':
    main()
