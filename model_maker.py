from src.classifiers.random_forest import RandomForest
from src.classifiers.svm_classifier import SVMClassifier
from src.classifiers.mlp_classifier import MLPClassifier

import pandas as pd
import numpy as np

from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import KFold

df = pd.read_csv('src/dataframe.csv', encoding='utf-8')
x = np.array(df.drop('common_answer', axis=1))
y = np.array(df['common_answer'])

avg_precision = 0
avg_recall = 0
avg_fscore = 0

repetitions = 50
n_splits = 10

for k in range(repetitions):
    # prepare cross validation
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=k)
    kf.get_n_splits(x)

    for train_index, test_index in kf.split(x):
        x_train, x_test = x[train_index], x[test_index]
        y_train, y_test = y[train_index], y[test_index]

        classifier = RandomForest(0)
        classifier.create_model(x_train, y_train)

        pred = classifier.predict(x_test)

        avg_precision += precision_recall_fscore_support(y_test, pred, average='weighted')[0]
        avg_recall += precision_recall_fscore_support(y_test, pred, average='weighted')[1]
        avg_fscore += precision_recall_fscore_support(y_test, pred, average='weighted')[2]

avg_precision /= (repetitions * n_splits)
avg_recall /= (repetitions * n_splits)
avg_fscore /= (repetitions * n_splits)

print('the results have been obtained doing the average of', repetitions, n_splits, '- fold cross validations')
print('average precision: ', avg_precision)
print('average recall: ', avg_recall)
print('average fscore: ', avg_fscore)
