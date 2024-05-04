import json
import numpy as np
from tqdm import tqdm


N_SIMULATIONS: int = 20000
PAYOFF_PER_UNIT: int = 200
START_MONTH: int = 4 # April
FIXED_PAYMENT: int = 30000
INTEREST_RATE: float = 2.87


def calculate_cvar(x: np.array, p: float) -> float:
    quantile = np.quantile(x, p)
    filtered = x[x > quantile]
    return float(filtered.mean())


def price_swap():
    simulated_prices = []
    for i in tqdm(range(1, N_SIMULATIONS + 1)):
        with open(f'simulations/sim_{i}.json', 'r') as file:
            data = json.loads(file.read())
            simulated_price = 0
            for month_sample in data:
                # calculate the monthly settlements
                this_month = month_sample['month']
                rainfall_this_month = month_sample['rainfall_count']
                floating_pmt_this_month = PAYOFF_PER_UNIT * rainfall_this_month
                simulated_price += floating_pmt_this_month / (1 + INTEREST_RATE / 100) ** ((this_month - START_MONTH + 1) / 12)
            simulated_prices.append(simulated_price)
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
    price_swap()
