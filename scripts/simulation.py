import calendar
from datetime import datetime, timedelta
import json
import numpy as np
from tqdm import tqdm


SIMULATION_YEAR = 2024
START_MONTH: int = 1
END_MONTH: int = 12


def sample_typhoon_counts(month: int) -> int:
    if 1 <= month <= 3:
        return 0
    else:
        match month:
            case 4:
                return np.random.binomial(1, 1/24)
            case 5:
                return np.random.binomial(1, 1/12)
            case 6:
                return np.random.binomial(2, 7/16)
            case 7:
                return np.random.binomial(3, 7/18)
            case 8:
                return np.random.binomial(3, 4/9)
            case 9:
                return np.random.binomial(3, 25/72)
            case 10:
                return np.random.binomial(3, 17/72)
            case 11:
                return np.random.binomial(1, 1/12)
            case 12:
                return np.random.binomial(1, 1/24)


def sample_typhoon_category() -> str:
    categories = ['1', '3', '8', '9&10']
    probs = [48/133, 44/133, 32/133, 9/133]
    return np.random.choice(categories, p=probs)


def generate_random_typhoon_days(category: str) -> int:
    if category in ['1', '3']:
        days_counts = list(range(1, 8))
        probs = [3/92, 48/92, 26/92, 12/92, 2/92, 0, 1/92]
        return int(np.random.choice(days_counts, p=probs))
    elif category in ['8', '9&10']:
        days_counts = list(range(1, 8))
        probs = [0, 6/41, 19/41, 13/41, 2/41, 1/41, 0]
        return int(np.random.choice(days_counts, p=probs))


def sample_typhoon_rainfall(category: str) -> float:
    match category:
        case '1':
            return np.random.binomial(1, 11/48) * np.random.gamma(1.3, 28.9)
        case '3':
            return np.random.gamma(1.2, 67.2)
        case '8':
            return np.random.gamma(1.6, 66.2)
        case '9&10':
            return np.random.gamma(3.9, 37.4)


def simulate(iter_count: int):
    start_date = datetime(SIMULATION_YEAR, START_MONTH, 1)
    current_date = start_date
    result = []
    np.random.seed(iter_count)
    for month in range(START_MONTH, END_MONTH + 1):
        month_sim_result = {}
        month_sim_result_list = []
        month_days = calendar.monthrange(SIMULATION_YEAR, month)[1]
        n_typhoons = sample_typhoon_counts(month)
        extreme_typhoon_count = 0
        typhoon_rainfall = 0
        if current_date.month != month:
            current_date = datetime(SIMULATION_YEAR, month, 1)
        for i in range(1, n_typhoons + 1):
            days_between = month_days - current_date.day
            typhoon_start_day = np.random.randint(current_date.day, current_date.day + days_between // n_typhoons * i + 1)
            current_date = datetime(SIMULATION_YEAR, month, typhoon_start_day)
            typhoon_start_date = datetime(SIMULATION_YEAR, month, typhoon_start_day).strftime('%Y/%m/%d')
            this_typhoon_category = sample_typhoon_category()
            if this_typhoon_category in ['8', '9&10']:
                extreme_typhoon_count += 1
            this_typhoon_days = generate_random_typhoon_days(this_typhoon_category)
            typhoon_end_date = (datetime(SIMULATION_YEAR, month, typhoon_start_day) + timedelta(days=this_typhoon_days - 1)).strftime('%Y/%m/%d')
            this_typhoon_rainfall = sample_typhoon_rainfall(this_typhoon_category)
            typhoon_rainfall += this_typhoon_rainfall
            current_date += timedelta(days=this_typhoon_days + 1)
            month_sim_result_list.append(
                {
                    "start_date": typhoon_start_date,
                    "end_date": typhoon_end_date,
                    "typhoon_days": this_typhoon_days,
                    "category": this_typhoon_category,
                    "rainfall": this_typhoon_rainfall
                }
            )
        month_sim_result["month"] = month
        month_sim_result["typhoon_count"] = n_typhoons
        month_sim_result["extreme_typhoon_count"] = extreme_typhoon_count
        month_sim_result["rainfall_count"] = typhoon_rainfall
        month_sim_result["details"] = month_sim_result_list
        result.append(month_sim_result)
    with open(f'simulations/sim_{iter_count}.json', 'w') as file:
        file.write(json.dumps(result, indent=4))


if __name__ == '__main__':
    n_simulations = 10000
    for i in tqdm(range(10001, 10000 + n_simulations + 1)):
        simulate(i)
