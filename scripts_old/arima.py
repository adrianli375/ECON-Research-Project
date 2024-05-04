import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error, \
    max_error
from statsmodels.tsa.arima.model import ARIMA
from tqdm import tqdm
from typing import Tuple


FILE_PATH = 'results/arima_model.txt'
SPLIT_DATE = '2023-01-01'
ORDERS = [ # (p, d, q)
    (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0), (0, 1, 1), (0, 1, 2), 
    (1, 0, 0), (1, 0, 1), (1, 0, 2), (1, 1, 0), (1, 1, 1), (1, 1, 2),
    (2, 0, 0), (2, 0, 1), (2, 0, 2), (2, 1, 0), (2, 1, 1), (2, 1, 2),
    (3, 0, 0), (3, 0, 1), (3, 0, 2), (3, 1, 0), (3, 1, 1), (3, 1, 2),
]


class ArimaModelProcess:
    def __init__(self):
        self.y_train = None
        self.y_test = None
        self.models = {}
        self.bics = {}
        self.best_model = None
        self.best_model_order = None
    
    def read_dataset(self):
        raw_df = pd.read_csv('HKO-Weather-Data-Interpolated.csv', usecols=['Date', 'TotalRainfall'])
        train_df = raw_df[raw_df['Date'] < SPLIT_DATE]
        test_df = raw_df[raw_df['Date'] >= SPLIT_DATE]
        self.y_train = train_df['TotalRainfall'].values
        self.y_test = test_df['TotalRainfall'].values
        self.y_pred = None

    def fit_model(self, order: Tuple[int]):
        model = ARIMA(self.y_train, order=order)
        result = model.fit()
        self.models[order] = result
        self.bics[order] = result.bic
    
    def evaluate(self):
        new_model = self.best_model.apply(self.y_test)
        self.y_pred = new_model.fittedvalues
        with open(FILE_PATH, 'a') as file:
            mse = mean_squared_error(self.y_test, self.y_pred)
            file.write(f'\nMean Squared Error = {mse}')
            rmse = np.sqrt(mse)
            file.write(f'\nRoot Mean Squared Error = {rmse}')
            mean_abs_err = mean_absolute_error(self.y_test, self.y_pred)
            file.write(f'\nMean Absolute Error = {mean_abs_err}')
            median_abs_err = median_absolute_error(self.y_test, self.y_pred)
            file.write(f'\nMedian Absolute Error = {median_abs_err}')
            max_err = max_error(self.y_test, self.y_pred)
            file.write(f'\nMax Error = {max_err}')
        
    def plot_extreme(self):
        start_idx, end_idx = 226, 288
        y_pred_sep = self.y_pred[start_idx:end_idx]
        y_test_sep = self.y_test[start_idx:end_idx]
        dates = pd.date_range(start='2023-08-15', end='2023-10-15', freq='D')
        plt.plot(dates, y_pred_sep, label='Predicted Rainfall')
        plt.plot(dates, y_test_sep, label='Actual Rainfall')
        plt.axvspan('2023-08-30', '2023-09-04', color='gray', alpha=0.5, linestyle='dotted')
        plt.axvspan('2023-09-05', '2023-09-10', color='gray', alpha=0.5, linestyle='dotted')
        plt.axvspan('2023-10-06', '2023-10-12', color='gray', alpha=0.5, linestyle='dotted')
        plt.xticks(dates[::14])
        plt.xlabel('Date')
        plt.ylabel('Daily Total Rainfall')
        plt.title('Rainfall in Hong Kong, 15/8/2023 to 15/10/2023')
        plt.legend()
        plt.savefig('figs/arima_prediction_error.png')

    def main(self):
        self.read_dataset()
        for i in tqdm(range(len(ORDERS))):
            order = ORDERS[i]
            self.fit_model(order=order)
        self.best_model_order = min(self.bics, key=lambda k: self.bics[k])
        self.best_model = self.models[self.best_model_order]
        with open(FILE_PATH, 'w') as file:
            file.write(str(self.best_model.summary()))
            file.write('\n----------------------------')
        self.evaluate()
        self.plot_extreme()


if __name__ == '__main__':
    process = ArimaModelProcess()
    process.main()
