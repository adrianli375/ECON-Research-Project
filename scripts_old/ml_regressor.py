from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import GammaRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, median_absolute_error, \
    max_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR


FILE_PATH = 'results/machine_learning_regressor.txt'
SPLIT_DATE = '2023-01-01'
RANDOM_STATE = 4200


class MachineLearningProcess:
    def __init__(self):
        self.file = open(FILE_PATH, 'w')
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.regressor = None
    
    def read_dataset(self):
        raw_df = pd.read_csv('HKO-Weather-Data-Interpolated.csv')
        raw_df['Date'] = pd.to_datetime(raw_df['Date'])
        raw_df.set_index('Date', inplace=True)
        raw_df['RainfallNextDay'] = raw_df['TotalRainfall'].shift(-1)
        raw_df.fillna(0, inplace=True) # next day (2024-01-01) has no rain
        train_df = raw_df[(raw_df.index < SPLIT_DATE) & (raw_df['RainfallNextDay'] > 0)]
        test_df = raw_df[(raw_df.index >= SPLIT_DATE) & (raw_df['RainfallNextDay'] > 0)]
        self.X_train = train_df.drop(columns=['Year', 'Month', 'Day', 'RainfallNextDay'])
        self.X_test = test_df.drop(columns=['Year', 'Month', 'Day', 'RainfallNextDay'])
        self.y_train = train_df['RainfallNextDay'].values
        self.y_test = raw_df[raw_df.index >= SPLIT_DATE]['RainfallNextDay'].values
        self.test_dates_with_rain = test_df.index
        self.y_pred = None
    
    def fit_regressor(self, model_name: str):
        if model_name not in {'dt', 'rf', 'svm', 'knn', 'gamma'}:
            raise ValueError(f'Invalid model_name argument: {model_name}!')
        self.file.write(f'\nModel name: {model_name}')
        match model_name:
            case 'dt':
                self.regressor = DecisionTreeRegressor(criterion='absolute_error', random_state=RANDOM_STATE)
            case 'rf':
                self.regressor = RandomForestRegressor(criterion='absolute_error', random_state=RANDOM_STATE)
            case 'svm':
                self.regressor = SVR(max_iter=5000)
            case 'knn':
                self.regressor = KNeighborsRegressor()
            case 'gamma':
                self.regressor = GammaRegressor(max_iter=5000)
        self.file.write(f'\n{datetime.now()} Training model...')
        self.regressor.fit(self.X_train, self.y_train)
        self.file.write(f'\n{datetime.now()} Training completed')
    
    def _pad_zeroes(self):
        start_date, end_date = '2023-01-01', '2023-12-31'
        new_date_index = pd.date_range(start_date, end_date, freq='D')
        self.y_pred = pd.Series(self.y_pred, index=self.test_dates_with_rain)
        self.y_pred = self.y_pred.reindex(new_date_index, fill_value=0).values
    
    def test_regressor(self):
        self.y_pred = self.regressor.predict(self.X_test)
        self._pad_zeroes()
        mse = mean_squared_error(self.y_test, self.y_pred)
        self.file.write(f'\nMean Squared Error = {mse}')
        rmse = np.sqrt(mse)
        self.file.write(f'\nRoot Mean Squared Error = {rmse}')
        mean_abs_err = mean_absolute_error(self.y_test, self.y_pred)
        self.file.write(f'\nMean Absolute Error = {mean_abs_err}')
        median_abs_err = median_absolute_error(self.y_test, self.y_pred)
        self.file.write(f'\nMedian Absolute Error = {median_abs_err}')
        max_err = max_error(self.y_test, self.y_pred)
        self.file.write(f'\nMax Error = {max_err}')
        self.file.write(f'\n------------------------')
    
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
        plt.savefig('figs/gamma_prediction_error.png')
    
    def main(self):
        self.file.write('Machine Learning Regressor Results: \n------------------------------')
        self.read_dataset()
        for model in ['dt', 'rf', 'svm', 'knn', 'gamma']:
            self.fit_regressor(model)
            self.test_regressor()
            if model == 'gamma':
                self.plot_extreme()
        self.file.close()


if __name__ == '__main__':
    process = MachineLearningProcess()
    process.main()
