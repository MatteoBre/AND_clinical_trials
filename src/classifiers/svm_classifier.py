from ..classifiers.classifier import Classifier
from sklearn import svm
from joblib import dump


class SVMClassifier(Classifier):

    def __init__(self):
        self.svm = None
        self.canSave = False

    def create_model(self, x_train, y_train):
        self.svm = svm.SVC()
        self.svm.fit(x_train, y_train)
        self.canSave = True

    def predict(self, x_test):
        pred = self.svm.predict(x_test)
        return pred

    def save_model_to_file(self, path):
        if self.canSave:
            dump(self.svm, path+'.joblib')
