import numpy as np
from sklearn import model_selection, svm, preprocessing
import pandas as pd
import pickle
import joblib


class LeapTrainer:
    def __init__(self, classifier_name, kernel_type, classifier=None, accuracy=0.0):
        self.accuracy = accuracy
        self.classifier = classifier
        self.classifier_name = classifier_name
        self.kernel_type = kernel_type

    def train_with_svm(self, csv_file):
        df = pd.read_csv(csv_file)
        df.replace('?', -99999, inplace=True)
        df.dropna(inplace=True)
        # Use all data except classification column
        X = np.array(df.drop(['class'], 1))
        # X = preprocessing.scale(X)

        df.dropna(inplace=True)
        # Use class column for classification
        y = np.array(df['class'])

        # Get training and test sets
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3)

        # Create SVM Classifier
        classifier = svm.SVC(kernel=self.kernel_type, probability=True)
        classifier.fit(X_train, y_train)
        # Check for accuracy produced from this classifier
        accuracy = classifier.score(X_test, y_test)

        self.accuracy = accuracy
        self.classifier = classifier


    #
    # def create_pickle(self, classifier, csv_without_ext):
    #     pickle_name = csv_without_ext + "saved.pickle"
    #     pickle_file = open(pickle_name, 'wb')
    #     pickle.dump(classifier, pickle_file)
    #
    #     print("Created : " +pickle_name)
    def save_classifier(self):
        pickle_name = self.classifier_name + "_" + self.kernel_type + ".pickle"
        # pickle_name = self.classifier_name + ".sav"
        pickle_file = open(pickle_name, 'wb')
        pickle.dump(self.classifier, pickle_file)
        # joblib.dump(self.classifier, pickle_name)

        print("Saving in : " + pickle_name)

    def load_classifier(self, pickle_name):
        pickle_file = open(pickle_name, 'rb')
        self.classifier = pickle.load(pickle_file)
        # self.classifier = joblib.load(pickle_file)

    def classify(self, X):
        prediction = self.classifier.predict(X)
        print "TEST : ", self.classifier.decision_function(X)
        print(prediction)
        return prediction

    def get_classifier(self):
        return self.classifier

    def get_accuracy(self):
        return self.accuracy
