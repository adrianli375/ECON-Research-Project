import json
import numpy as np
from tqdm import tqdm


N_SIMULATIONS: int = 20000
MONTH: int = 7 # July
PAYOFF_PER_UNIT: int = 200
STRIKE: int = 250


def calculate_cvar(x: np.array, p: float) -> float:
    quantile = np.quantile(x, p)
    filtered = x[x > quantile]
    return float(filtered.mean())


def price_call_option():
    simulated_prices = []
    for i in tqdm(range(1, N_SIMULATIONS + 1)):
        with open(f'simulations/sim_{i}.json', 'r') as file:
            data = json.loads(file.read())
            for month_sample in data:
                if month_sample['month'] == MONTH:
                    rainfall = month_sample['rainfall_count']
                    payoff = PAYOFF_PER_UNIT * max(rainfall - STRIKE, 0)
                    simulated_prices.append(payoff)
                    continue
    assert len(simulated_prices) == N_SIMULATIONS
    simulated_prices = np.array(simulated_prices)
    average = simulated_prices.mean()
    print(f'Mean = {average}')
    std = simulated_prices.std()
    print(f'SD = {std}')
    minimum, maximum = simulated_prices.min(), simulated_prices.max()
    print(f'min = {minimum}, max = {maximum}')
    q = 0.95
    quantile = np.quantile(simulated_prices, q)
    print(f'{int(q * 100)}% percentile = {quantile}')
    cvar = calculate_cvar(simulated_prices, q)
    print(f'{int(q * 100)}% conditional VaR = {cvar}')


if __name__ == '__main__':
    price_call_option()
