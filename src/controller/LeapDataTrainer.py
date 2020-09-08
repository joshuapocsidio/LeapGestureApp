import pickle
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import leapio.LeapIO as io


class Trainer:
    def __init__(self, subject_name, classifier_name, feature_type):
        self.subject_name = subject_name
        self.classifier = None
        self.classifier_name = classifier_name
        self.feature_type = feature_type
        self.training_acc = 0.0
        self.testing_acc = 0.0
        self.std_scale = None
        pass

    def save(self, pickle_name):
        io.save_classifier(pickle_name=pickle_name, data=self.classifier)
        io.save_scale(pickle_name=pickle_name, data=self.std_scale)
        pass

    def load(self, pickle_name):
        self.classifier = io.load_classifier(pickle_name=pickle_name)
        self.std_scale = io.load_scale(pickle_name)
        ''' UNCOMMENT FOR DEBUGGING
        # print self.classifier
        # print self.std_scale
        '''

        pass

    def classify(self, X):
        X = self.std_scale.transform(X)
        prediction = self.classifier.predict(X)

        ''' UNCOMMENT FOR DEBUGGING
        # print("SCALED : " + str(X))
        # print(self.classifier.predict_log_proba(X))
        # print(self.classifier.decision_function(X))
        '''
        return prediction

    def get_normalized_data(self, csv_file):
        # Read csv file
        data = pd.read_csv(csv_file)
        X = np.array(data.drop(['class'], 1))
        y = np.array(data['class'])

        # Split data
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.3)

        # Normalize input data
        X_train, X_test = self._normalize_data(train_data=X_train, test_data=X_test)

        # Get unique classifications
        y_unique = np.unique(y)

        return X_train, X_test, y_train, y_test, y_unique

    def _normalize_data(self, train_data, test_data):
        # Normalize data with standard scaler
        self.std_scale = StandardScaler()
        self.std_scale.fit(train_data)
        X_train = self.std_scale.transform(train_data)
        X_test = self.std_scale.transform(test_data)

        return X_train, X_test

class DT_Trainer(Trainer):
    def __init__(self, subject_name, feature_type, classifier_name):
        Trainer.__init__(
            self,
            subject_name,
            classifier_name,
            feature_type
        )
        self.criterion = None
        self.splitter = None
        pass

    def train(self, csv_file):
        # Read data from csv and Split data into training and testing data
        X_train, X_test, y_train, y_test, y_unique = self.get_normalized_data(csv_file=csv_file)

        # Build SVM Classifier
        classifier = DecisionTreeClassifier()

        # Initialize configurations of hyper parameters
        grid_parameters = {
            'criterion': ['gini', 'entropy'],
            'splitter': ['best', 'random'],
        }
        # Initialize hyper parameter tuning grid search
        grid_classifier = GridSearchCV(classifier, grid_parameters, n_jobs=4, cv=5)
        # Fit the model
        grid_classifier.fit(X_train, y_train)

        self.training_acc = grid_classifier.best_score_
        self.testing_acc = grid_classifier.score(X_test, y_test)
        self.classifier = grid_classifier.best_estimator_
        self.classifier.fit(X_train, y_train)
        # print(self.classifier.score(X_test, y_test))

        # Hyper Parameters
        self.criterion = grid_classifier.best_params_['criterion']
        self.splitter = grid_classifier.best_params_['splitter']
        pass

    def save_classifier(self):
        pickle_name = "(" + self.subject_name + ") SVM_" + self.feature_type + "_" + self.criterion + "_" + self.splitter + ".pickle"
        # print("Saving in : " + pickle_name)
        self.save(pickle_name=pickle_name)
        pass


class RF_Trainer(Trainer):
    def __init__(self, subject_name, feature_type, classifier_name):
        Trainer.__init__(
            self,
            subject_name,
            classifier_name,
            feature_type
        )
        pass


class NN_Trainer(Trainer):
    def __init__(self, subject_name, feature_type, activation, optimizer):
        Trainer.__init__(
            self,
            subject_name=subject_name,
            classifier_name="Multi-Layer Perceptron Neural Network",
            feature_type=feature_type
        )
        self.batch_size = 0
        self.activation = activation
        self.optimizer = optimizer
        self.n_layers = 0
        self.n_layer_nodes = [()]
        self.learning_rate = 0.0
        pass

    def train(self, csv_file):
        # Read data from csv and Split data into training and testing data
        X_train, X_test, y_train, y_test, y_unique = self.get_normalized_data(csv_file=csv_file)

        self.batch_size = len(X_train[0])

        # Build neural network classifier
        classifier = MLPClassifier(
            shuffle=True,
            verbose=False,
            batch_size=self.batch_size,
            max_iter=1000
        )

        # Initialize configurations of hyper parameters
        grid_parameters = {
            'learning_rate_init': [0.01, 0.05, 0.1, 0.5],
            'hidden_layer_sizes': [(64,), (128,), (64, 64,), (128, 128,), (64, 128, 128, 64)]
        }
        # Initialize hyper parameter tuning grid search
        grid_classifier = GridSearchCV(classifier, grid_parameters, n_jobs=4, cv=5)
        # Fit the model
        grid_classifier.fit(X_train, y_train)

        self.training_acc = grid_classifier.best_score_
        self.testing_acc = grid_classifier.score(X_test, y_test)
        self.classifier = grid_classifier.best_estimator_

        self.classifier.fit(X_train, y_train)

        # Hyper Parameters
        self.n_layers = len(grid_classifier.best_params_['hidden_layer_sizes'])
        self.n_layer_nodes = grid_classifier.best_params_['hidden_layer_sizes']
        self.learning_rate = grid_classifier.best_params_['learning_rate_init']
        pass

    def save_classifier(self):
        pickle_name = "(" + self.subject_name + ") NN_" + self.feature_type + "_" + self.activation + "_" + self.optimizer + ".pickle"
        # print("Saving in : " + pickle_name)
        self.save(pickle_name=pickle_name)
        pass


class SVM_Trainer(Trainer):
    def __init__(self, subject_name, feature_type, kernel_type):
        Trainer.__init__(
            self,
            subject_name=subject_name,
            classifier_name="Support Vector Machine",
            feature_type=feature_type,
        )

        self.kernel_type = kernel_type
        self.c_param = 0.1
        pass

    def train(self, csv_file):
        # Read data from csv and Split data into training and testing data
        X_train, X_test, y_train, y_test, y_unique = self.get_normalized_data(csv_file=csv_file)

        # Build SVM Classifier
        classifier = SVC(kernel=self.kernel_type, probability=True)

        # Initialize configurations of hyper parameters
        grid_parameters = {
            'C': [0.1, 1.0, 10.0],
        }
        # Initialize hyper parameter tuning grid search
        grid_classifier = GridSearchCV(classifier, grid_parameters, n_jobs=4, cv=5)
        # Fit the model
        grid_classifier.fit(X_train, y_train)

        self.training_acc = grid_classifier.best_score_
        self.testing_acc = grid_classifier.score(X_test, y_test)
        self.classifier = grid_classifier.best_estimator_
        self.classifier.fit(X_train, y_train)
        # print(self.classifier.score(X_test, y_test))

        # Hyper Parameters
        self.c_param = grid_classifier.best_params_['C']
        pass

    def save_classifier(self):
        pickle_name = "(" + self.subject_name + ") SVM_" + self.feature_type + "_" + self.kernel_type + ".pickle"
        # print("Saving in : " + pickle_name)
        self.save(pickle_name=pickle_name)
        pass
