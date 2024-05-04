from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


FILE_PATH = 'results/machine_learning_classifier.txt'
SPLIT_DATE = '2023-01-01'
RANDOM_STATE = 4200


class MachineLearningProcess:
    def __init__(self):
        self.file = open(FILE_PATH, 'w')
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.classifier = None
    
    def read_dataset(self):
        raw_df = pd.read_csv('HKO-Weather-Data-Interpolated.csv')
        raw_df['Date'] = pd.to_datetime(raw_df['Date'])
        raw_df.set_index('Date', inplace=True)
        raw_df['HasRain'] = raw_df['TotalRainfall'].apply(lambda x: 1 if x > 0 else 0)
        raw_df['RainOnNextDay'] = raw_df['HasRain'].shift(-1)
        raw_df.fillna(0, inplace=True) # next day (2024-01-01) has no rain
        train_df = raw_df[raw_df.index < SPLIT_DATE]
        test_df = raw_df[raw_df.index >= SPLIT_DATE]
        self.X_train = train_df.drop(columns=['Year', 'Month', 'Day', 'TotalRainfall', 'HasRain', 'RainOnNextDay'])
        self.X_test = test_df.drop(columns=['Year', 'Month', 'Day', 'TotalRainfall', 'HasRain', 'RainOnNextDay'])
        self.y_train = train_df['RainOnNextDay'].values
        self.y_test = test_df['RainOnNextDay'].values
        self.y_pred = None
    
    def fit_classifier(self, model_name: str):
        if model_name not in {'dt', 'rf', 'svm', 'knn', 'lr'}:
            raise ValueError(f'Invalid model_name argument: {model_name}!')
        self.file.write(f'\nModel name: {model_name}')
        match model_name:
            case 'dt':
                self.classifier = DecisionTreeClassifier(class_weight='balanced', random_state=RANDOM_STATE)
            case 'rf':
                self.classifier = RandomForestClassifier(class_weight='balanced', random_state=RANDOM_STATE)
            case 'svm':
                self.classifier = SVC(C=1, class_weight='balanced', random_state=RANDOM_STATE) # optimize on C and gamma?
            case 'knn':
                self.classifier = KNeighborsClassifier()
            case 'lr':
                self.classifier = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=RANDOM_STATE) # optimize on C?
        self.file.write(f'\n{datetime.now()} Training model...')
        self.classifier.fit(self.X_train, self.y_train)
        self.file.write(f'\n{datetime.now()} Training completed')
    
    def test_classifier(self):
        y_pred = self.classifier.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        self.file.write(f'\nAccuracy = {accuracy}')
        precision = precision_score(self.y_test, y_pred)
        self.file.write(f'\nPrecision = {precision}')
        recall = recall_score(self.y_test, y_pred)
        self.file.write(f'\nRecall = {recall}')
        f1 = f1_score(self.y_test, y_pred)
        self.file.write(f'\nf1 = {f1}')
        cm = confusion_matrix(self.y_test, y_pred)
        self.file.write(f'\nConfusion matrix: \n{cm}')
        self.file.write(f'\n------------------------')
    
    def main(self):
        self.file.write('Machine Learning Classifier Results: \n------------------------------')
        self.read_dataset()
        for model in ['dt', 'rf', 'svm', 'knn', 'lr']:
            self.fit_classifier(model)
            self.test_classifier()
        self.file.close()


if __name__ == '__main__':
    process = MachineLearningProcess()
    process.main()
