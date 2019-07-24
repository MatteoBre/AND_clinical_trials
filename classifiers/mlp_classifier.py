import classifiers.classifier as classifier
from sklearn import neural_network
from joblib import dump


class MLPClassifier(classifier.Classifier):

    def __init__(self, random_state, sizes):
        self.mlp = None
        self.sizes = sizes
        self.canSave = False
        self.random_state = random_state

    def create_model(self, x_train, y_train):
        self.mlp = neural_network.MLPClassifier(random_state=self.random_state, hidden_layer_sizes=self.sizes)
        self.mlp.fit(x_train, y_train)
        self.canSave = True

    def predict(self, x_test):
        pred = self.mlp.predict(x_test)
        return pred

    def save_model_to_file(self, path):
        if self.canSave:
            dump(self.mlp, path+'.joblib')
