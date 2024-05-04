import numpy as np
import pandas as pd
from scipy.stats import gamma, kstest

HIGHEST_SIGNALS = ['1', '3', '8', '9&10', '8&9&10']


def main():
    with open('results/rainfall_dist_fit.txt', 'w') as file:
        df = pd.read_csv('HKO-Typhoon-History.csv', dtype={'MaxSignal': str})
        for sig in HIGHEST_SIGNALS:
            if sig not in ['9&10', '8&9&10']:
                sub_df = df[df['MaxSignal'] == sig]
            elif sig == '9&10':
                sub_df = df[df['MaxSignal'].isin(['9', '10'])]
            elif sig == '8&9&10':
                sub_df = df[df['MaxSignal'].isin(['8', '9', '10'])]
            obs = sub_df['TotalRainfall'].values
            if sig != '1':
                # fit to a gamma distribution, where
                # mean = \alpha * \theta, variance = \alpha * \theta ** 2
                # using method of moments, \theta = variance / mean, and
                # \alpha = mean / \theta
                mean, var = obs.mean(), obs.var(ddof=1)
                theta = var / mean
                alpha = mean / theta
                res = kstest(obs, gamma(a=alpha, scale=theta).cdf)
                file.write(f'Signal: {sig}, Fitted distribution: Gamma, \n'
                           f'alpha = {alpha}, theta (scale) = {theta} \n'
                           f'KS-Test: statistic = {res.statistic}, p-value = {res.pvalue}\n--------\n')
            else:
                # fit to a mixed gamma distribution
                print(obs)
                obs_count = obs.size
                zero_count = obs[obs == 0].size
                p = zero_count / obs_count
                non_zero_obs = obs[obs != 0]
                mean, var = non_zero_obs.mean(), non_zero_obs.var(ddof=1)
                theta = var / mean
                alpha = mean / theta
                res = kstest(non_zero_obs, gamma(a=alpha, scale=theta).cdf)
                file.write(f'Signal: {sig}, Fitted distribution: 0 (w.p. {p:.2f}) & Gamma (w.p. {1-p:.2f}), \n'
                           f'alpha = {alpha}, theta (scale) = {theta} \n'
                           f'KS-Test: statistic = {res.statistic}, p-value = {res.pvalue}\n--------\n')


if __name__ == '__main__':
    main()
