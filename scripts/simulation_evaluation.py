import json
import pandas as pd
from tqdm import tqdm


N_SIMULATIONS: int = 20000
TOTAL_MONTHS: int = 12


def get_first_typhoon_date(data: dict) -> str:
    for i in range(TOTAL_MONTHS):
        month_data = data[i]
        try:
            first_date = month_data['details'][0]['start_date']
            return first_date
        except IndexError:
            continue


def get_last_typhoon_date(data: dict) -> str:
    for i in range(TOTAL_MONTHS - 1, -1, -1):
        month_data = data[i]
        try:
            last_date = month_data['details'][-1]['end_date']
            return last_date
        except IndexError:
            continue


def evaluate():
    typhoon_counts = []
    extreme_typhoon_counts = []
    rainfall = []
    first_typhoon_dates = []
    last_typhoon_dates = []
    for i in tqdm(range(1, N_SIMULATIONS + 1)):
        with open(f'simulations/sim_{i}.json', 'r') as file:
            data = json.loads(file.read())
        sim_typhoon_counts = sum([month["typhoon_count"] for month in data])
        sim_extreme_typhoon_counts = sum([month["extreme_typhoon_count"] for month in data])
        sim_rainfall_total = sum([month["rainfall_count"] for month in data])
        first_typhoon_date = get_first_typhoon_date(data)
        last_typhoon_date = get_last_typhoon_date(data)
        typhoon_counts.append(sim_typhoon_counts)
        extreme_typhoon_counts.append(sim_extreme_typhoon_counts)
        rainfall.append(sim_rainfall_total)
        first_typhoon_dates.append(first_typhoon_date)
        last_typhoon_dates.append(last_typhoon_date)
    output_df = pd.DataFrame(columns=['SimNumber', 'TyphoonCount', 'ExtremeTyphoonCount', 'Rainfall', 'FirstTyphoonDate', 'LastTyphoonDate'])
    output_df['SimNumber'] = range(1, N_SIMULATIONS + 1)
    output_df['TyphoonCount'] = typhoon_counts
    output_df['ExtremeTyphoonCount'] = extreme_typhoon_counts
    output_df['Rainfall'] = rainfall
    output_df['FirstTyphoonDate'] = first_typhoon_dates
    output_df['LastTyphoonDate'] = last_typhoon_dates
    output_df.to_csv(f'raw-data/simulation_eval_{N_SIMULATIONS}.csv', index=False)


if __name__ == '__main__':
    evaluate()