import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def get_correlation_output():
    df = pd.read_csv('HKO-Weather-Data-Interpolated.csv', 
                     usecols=['MeanCloudAmount', 'MeanPressure', 'TotalEvaporation', 
                              'TotalRainfall', 'MeanHumidity', 'MinTemperature', 
                              'MeanTemperature', 'MaxTemperature', 'MeanUVIndex', 
                              'TotalSunshine', 'MeanWindSpeed', 'IsExtreme'])
    corr_matrix = df.corr()
    plt.figure(figsize=(15, 15))
    sns.heatmap(corr_matrix, annot=True)
    # plt.show()
    # fix figure dimension problem
    plt.savefig('figs/correlation.png')


if __name__ == '__main__':
    get_correlation_output()
