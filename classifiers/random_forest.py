import classifiers.classifier as classifier
from sklearn.ensemble import RandomForestClassifier
from joblib import dump


class RandomForest(classifier.Classifier):

    def __init__(self):
        self.rfc = None
        self.canSave = False

    def create_model(self, x_train, y_train):
        self.rfc = RandomForestClassifier(n_estimators=500)
        self.rfc.fit(x_train, y_train)
        self.canSave = True

    def predict(self, x_test):
        pred = self.rfc.predict(x_test)
        return pred

    def save_model_to_file(self, path):
        if self.canSave:
            dump(self.rfc, path+'.joblib')
