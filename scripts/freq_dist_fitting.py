from math import isclose
import numpy as np
import pandas as pd
from scipy.stats import poisson, binom, nbinom, chisquare

MONTHS_TO_FIT = ['Apr', 'May', 'Jun', 'Jul', 'Aug',
                 'Sep', 'Oct', 'Nov', 'Dec']

def main():
    with open('results/frequency_dist_fit.txt', 'w') as file:
        df = pd.read_excel('raw-data/typhoon_count.xlsx')
        for month in MONTHS_TO_FIT:
            obs = df[month].to_numpy()
            mean, var = obs.mean(), obs.var(ddof=1)
            file.write(f'{month}: Mean = {mean}, Variance = {var}\n')
            # ---1. if mean = var => poisson
            # if isclose(mean, var):
            #     mu = mean
            #     f_obs = np.append(np.bincount(obs), 0)
            #     f_exp = np.array([poisson.pmf(k, mu) * obs.size for k in np.unique(obs)])
            #     f_exp = np.append(f_exp, obs.size - f_exp.sum())
            #     res = chisquare(f_obs, f_exp)
            #     file.write(f'Fitted distribution: Poisson, lambda = {mu} \n'
            #         f'Goodness of fit: chi2 = {res.statistic}, p-value = {res.pvalue}\n---------\n')
            # ---2. if mean > var => binom
            # else:
            n = obs.max()
            p = mean / n
            f_obs = np.bincount(obs)
            f_exp = np.array([binom.pmf(k, n, p) * obs.size for k in np.arange(len(f_obs))])
            res = chisquare(f_obs, f_exp)
            file.write(f'Fitted distribution: Binomial, n = {n}, p = {p} \n'
                f'Goodness of fit: chi2 = {res.statistic}, p-value = {res.pvalue}\n---------\n')
            # ---3. if mean < var => nbinom
            # else:
            #     n = mean ** 2 / (var - mean)
            #     p = mean / var
            #     f_obs = np.append(np.bincount(obs), 0)
            #     f_exp = np.array([nbinom.pmf(k, n, p) * obs.size for k in np.arange(len(f_obs)-1)])
            #     f_exp = np.append(f_exp, obs.size - f_exp.sum())
            #     res = chisquare(f_obs, f_exp)
            #     file.write(f'Fitted distribution: Negative Binomial, n = {n}, p = {p} \n'
            #           f'Goodness of fit: chi2 = {res.statistic}, p-value = {res.pvalue}')


if __name__ == '__main__':
    main()
