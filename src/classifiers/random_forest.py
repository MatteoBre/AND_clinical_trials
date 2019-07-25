from ..classifiers.classifier import Classifier
from sklearn.ensemble import RandomForestClassifier
from joblib import dump


class RandomForest(Classifier):

    def __init__(self, random_state):
        self.rfc = None
        self.canSave = False
        self.random_state = random_state

    def create_model(self, x_train, y_train):
        self.rfc = RandomForestClassifier(random_state=self.random_state, n_estimators=500, max_depth=None,
                                          min_samples_split=2, max_features='auto')
        self.rfc.fit(x_train, y_train)
        self.canSave = True

    def predict(self, x_test):
        pred = self.rfc.predict(x_test)
        return pred

    def save_model_to_file(self, path):
        if self.canSave:
            dump(self.rfc, path+'.joblib')
