import numpy as np
import pandas as pd
import statsmodels.api as sm


def run_simple_regression():
    df = pd.read_csv('HKO-Weather-Data-Interpolated.csv', 
                     usecols=['MeanCloudAmount', 'MeanPressure', 'TotalEvaporation', 
                              'TotalRainfall', 'MeanHumidity', 
                              'MeanTemperature', 'MeanUVIndex', 
                              'TotalSunshine', 'MeanWindSpeed'])
    endog = df['TotalRainfall']
    exog = df[['MeanCloudAmount', 'MeanPressure', 'TotalEvaporation', 
            'MeanHumidity', 'MeanTemperature', 'MeanUVIndex', 
            'TotalSunshine', 'MeanWindSpeed']]
    exog = sm.add_constant(exog)
    model = sm.OLS(endog, exog)
    result = model.fit()
    summary = result.summary().as_text()
    with open('results/regression_base.txt', 'w') as file:
        file.write(summary)


def run_log_regression():
    df = pd.read_csv('HKO-Weather-Data-Interpolated.csv', 
                     usecols=['MeanCloudAmount', 'MeanPressure', 'TotalEvaporation', 
                              'TotalRainfall', 'MeanHumidity', 
                              'MeanTemperature', 'MeanUVIndex', 
                              'TotalSunshine', 'MeanWindSpeed'])
    endog = np.log(1 + df['TotalRainfall'])
    exog = df[['MeanCloudAmount', 'MeanPressure', 'TotalEvaporation', 
            'MeanHumidity', 'MeanTemperature', 'MeanUVIndex', 
            'TotalSunshine', 'MeanWindSpeed']]
    exog = sm.add_constant(exog)
    model = sm.OLS(endog, exog)
    result = model.fit()
    summary = result.summary().as_text()
    with open('results/regression_log.txt', 'w') as file:
        file.write(summary)


if __name__ == '__main__':
    run_simple_regression()
    run_log_regression()
