import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from utils import utils

class trainProductsClassifier(object):

    def __init__(self, show_confusion_matrix=True):
        self.confusion_matrix = show_confusion_matrix
        self.train_model()

    def train_model(self):
        model_path, _ = utils.create_saved_model_folder('food_model')

        dataframe, y = self.get_data(model_path)
        X = self.get_previsors_attrib(dataframe, model_path)
        
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.3,
                                                            stratify=y) 

        cnn = utils.create_model_instance(y, self.tokenizer.vocab_size)
        cnn.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model_path + '/model_checkpoint/cp.ckpt',
                                                        save_weights_only=True,
                                                        verbose=1)

        cnn.fit(X_train, y_train,
                batch_size = 64,
                epochs = 1,
                verbose = 1,
                validation_split = 0.10,
                callbacks=[cp_callback])

        utils.evaluate_model(cnn, X_test, y_test)

        if self.confusion_matrix:
            self.predict_and_plot_matrix(cnn, X_test, y_test)

    def get_data(self, model_path):
        dataframe = pd.read_excel('./src/utils/datasets/positive_and_negative_food.xlsx')

        y = utils.encode_class_value(
            dataframe['Category'].values, model_path + '/label_encoder.pkl')

        print('Dataframe read')
        sys.stdout.flush()
        return dataframe, y

    def get_previsors_attrib(self, dataframe, model_path): 
        product_name = [[x] for x in dataframe['name']]

        X = list(map(utils.get_description_and_name, product_name))

        X, self.tokenizer = utils.preprocessing_fn(
            X, model_path + '/token')

        return X

    def predict_and_plot_matrix(self, cnn, X_test, y_test):
        y_pred_test = cnn.predict(X_test)
        y_pred_test[y_pred_test > 0.5] = 1
        y_pred_test[y_pred_test <= 0.5] = 0
        utils.show_confusion_matrix(y_test, y_pred_test)

trainProductsClassifier()
