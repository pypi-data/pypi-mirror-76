import sys
import os
from sys import argv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow as tf
from sklearn.model_selection import train_test_split
import tensorflow_datasets as tfds
import shutil
import subprocess

from utils import utils
from database.db_mongo import MongoDatabase

class trainProductsClassifier(object):

    def __init__(self, environment, show_confusion_matrix=False):
        self.environment = environment
        self.confusion_matrix = show_confusion_matrix
        self.train_model()

    def train_model(self):
        model_path, last_model_path = utils.create_saved_model_folder('category_model')
        dataframe, y = self.get_data(model_path)
        X = self.get_previsors_attrib(dataframe, model_path)
        
        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.3,
                                                            random_state=1) 

        cnn = utils.create_model_instance(y, self.tokenizer)
        cnn.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=model_path + '/model_checkpoint/cp.ckpt',
                                                        save_weights_only=True,
                                                        verbose=1)
        cnn.fit(X_train, y_train,
                batch_size = 64,
                epochs = 1,
                verbose = 1,
                validation_split = 0.10,
                callbacks=[cp_callback])

        model_version = '{"version": "%s"}' %(model_path.split('/')[-1])
        if last_model_path:
            last_model_accuracy = self.get_last_model_accuracy(
                last_model_path, X_test, y_test, y)

            new_model_accuracy = utils.evaluate_model(cnn, X_test, y_test)
            if new_model_accuracy >= last_model_accuracy:
                shutil.rmtree(last_model_path)
                utils.read_file(os.getcwd() + '/config.txt', model_version)
                subprocess.call(os.getcwd() + '/pypi-upload.sh')
            else: 
                shutil.rmtree(model_path)
        else:
            utils.read_file(os.getcwd() + '/config.txt', model_version)

        if self.confusion_matrix:
            self.predict_and_plot_matrix(cnn, X_test, y_test)

    def get_data(self, model_path):
        self.open_mongo_connections()
        dataframe = utils.get_dataframe_from_mongo(self.mongo_conn)
        self.close_mongo_connection()

        dataframe['description'].fillna('', inplace=True)

        y = utils.encode_class_value(
            dataframe['Category'].values, model_path + '/label_encoder.pkl')

        print('Restored data from Mongo')
        sys.stdout.flush()
        return dataframe, y

    def open_mongo_connections(self):
        self.mongo = MongoDatabase(self.environment)
        self.mongo.connect()
        self.mongo_conn = self.mongo

    def close_mongo_connection(self):
        self.mongo.close_connection()

    def get_previsors_attrib(self, dataframe, model_path):
        ingredients = [x for x in dataframe['ingredients']] 
        # allergics = [x for x in dataframe['allergics']]
        description = [[x] for x in dataframe['description']]
        product_name = [[x] for x in dataframe['name']]

        X = utils.get_cleaned_predictor(ingredients, [], description, product_name)
        
        X, self.tokenizer = utils.preprocessing_fn(
            X, model_path + '/token')

        return X

    def get_last_model_accuracy(self, last_model_path, X_test, y_test, y):
        tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(last_model_path + '/token')

        last_cnn = utils.create_model_instance(y, tokenizer)
        last_cnn.load_weights(last_model_path + '/model_checkpoint/cp.ckpt').expect_partial()

        last_cnn.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return utils.evaluate_model(last_cnn, X_test, y_test)

    def predict_and_plot_matrix(self, model, X, y):
        y_pred_test = model.predict(X)
        predicted = [result.argmax() for result in y_pred_test]
        utils.show_confusion_matrix(y, predicted)
        
trainProductsClassifier(argv[1] if len(argv) > 1 else 'dev')
