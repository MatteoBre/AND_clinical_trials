import unittest
import numpy as np
import pandas as pd
import os
from src.classifiers.random_forest import RandomForest
from sklearn.model_selection import train_test_split
from src.classifiers.svm_classifier import SVMClassifier
from src.classifiers.mlp_classifier import MLPClassifier


class TestClassifiers(unittest.TestCase):
    df = pd.read_csv('src/dataframe.csv', encoding='utf-8')
    x = np.array(df.drop('common_answer', axis=1))
    y = np.array(df['common_answer'])
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=1)

    def test_random_forest(self):
        try:
            classifier = RandomForest(0)
            classifier.create_model(self.x_train, self.y_train)
            classifier.predict(self.x_test)
            if not os.path.exists('test/test_models/'):
                os.makedirs('test/test_models/')
            classifier.save_model_to_file('test/test_models/random_forest')
            classifier.get_importance()
        except:
            self.assertTrue(False)

    def test_svm_classifier(self):
        try:
            classifier = SVMClassifier(0)
            classifier.create_model(self.x_train, self.y_train)
            classifier.predict(self.x_test)
            if not os.path.exists('test/test_models/'):
                os.makedirs('test/test_models/')
            classifier.save_model_to_file('test/test_models/svm_classifier')
        except:
            self.assertTrue(False)

    def test_mlp_classifier(self):
        try:
            classifier = MLPClassifier(0)
            classifier.create_model(self.x_train, self.y_train)
            classifier.predict(self.x_test)
            if not os.path.exists('test/test_models/'):
                os.makedirs('test/test_models/')
            classifier.save_model_to_file('test/test_models/svm_classifier')
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
