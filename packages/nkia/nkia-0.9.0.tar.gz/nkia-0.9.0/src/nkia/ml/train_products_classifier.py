import sys
import os
import os.path
from sys import argv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow as tf
from sklearn.model_selection import train_test_split
import tensorflow_datasets as tfds
import shutil
import subprocess
import tarfile

from utils import utils
from database.db_mongo import MongoDatabase
from nkia.ml.deploy_model import DeployModel

class trainProductsClassifier(object):

    def __init__(self, environment, show_confusion_matrix=False):
        self.environment = environment
        self.confusion_matrix = show_confusion_matrix
        self.model_path, self.last_model_path = utils.create_saved_model_folder('category_model')
        self.train_model()

    def train_model(self):
        dataframe, y = self.get_data()
        X = self.get_previsors_attrib(dataframe)

        X_train, X_test, y_train, y_test = train_test_split(X,
                                                            y,
                                                            test_size=0.3,
                                                            random_state=1,
                                                            stratify=y) 

        cnn = utils.create_model_instance(y, self.tokenizer.vocab_size)
        cnn.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.model_path + '/model_checkpoint/cp.ckpt',
                                                        save_weights_only=True,
                                                        verbose=1)
        cnn.fit(X_train, y_train,
                batch_size = 64,
                epochs = 2,
                verbose = 1,
                validation_split = 0.10,
                callbacks=[cp_callback])

        self.evaluate_and_deploy_model(cnn, X_test, y_test, y)
        
        if self.confusion_matrix:
            self.predict_and_plot_matrix(cnn, X_test, y_test)

    def get_data(self):
        self.open_mongo_connections()
        dataframe = utils.get_dataframe_from_mongo(self.mongo_conn)
        self.close_mongo_connection()

        dataframe['description'].fillna('', inplace=True)

        y = utils.encode_class_value(
            dataframe['Category'].values, self.model_path + '/label_encoder.pkl')

        print('Restored data from Mongo')
        sys.stdout.flush()
        return dataframe, y

    def open_mongo_connections(self):
        self.mongo = MongoDatabase(self.environment)
        self.mongo.connect()
        self.mongo_conn = self.mongo

    def close_mongo_connection(self):
        self.mongo.close_connection()

    def get_previsors_attrib(self, dataframe):
        ingredients = [x for x in dataframe['ingredients']] 
        # allergics = [x for x in dataframe['allergics']]
        description = [[x] for x in dataframe['description']]
        product_name = [[x] for x in dataframe['name']]

        X = utils.get_cleaned_predictor(ingredients, [], description, product_name)
        
        X, self.tokenizer = utils.preprocessing_fn(
            X, self.model_path + '/token')

        return X

    def get_last_model_performance(self, last_model_path, X_test, y_test, y):
        tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(last_model_path + '/token')

        last_cnn = utils.create_model_instance(y, tokenizer.vocab_size + 1) # +1 por que load_from_file reduz o vocab_size real em 1.
        last_cnn.load_weights(last_model_path + '/model_checkpoint/cp.ckpt').expect_partial()

        last_cnn.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return utils.evaluate_model(last_cnn, X_test, y_test)

    def predict_and_plot_matrix(self, model, X, y):
        y_pred_test = model.predict(X)
        predicted = [result.argmax() for result in y_pred_test]
        utils.show_confusion_matrix(y, predicted)

    def evaluate_and_deploy_model(self, cnn, X_test, y_test, y):
        model_version = '{"version": "%s"}' %(self.model_path.split('/')[-1])
        if self.last_model_path:
            new_model_accuracy, new_model_f1 = utils.evaluate_model(cnn, X_test, y_test)

            last_model_accuracy, last_model_f1 = self.get_last_model_performance(
                self.last_model_path, X_test, y_test, y)

            if new_model_f1 >= last_model_f1 and (new_model_accuracy - last_model_accuracy) < 1:
                shutil.rmtree(self.last_model_path)
                utils.read_file(os.getcwd() + '/config.txt', model_version)
                self.create_and_deploy_tarfile(self.model_path + '.tar.gz', self.model_path)
                subprocess.call(os.getcwd() + '/pypi-upload.sh')
            else: 
                shutil.rmtree(self.model_path)
        else:
            utils.read_file(os.getcwd() + '/config.txt', model_version)
            self.create_and_deploy_tarfile(self.model_path + '.tar.gz', self.model_path)
            subprocess.call(os.getcwd() + '/pypi-upload.sh') # O correto é não existir esse else, mas baixar a útima versão sempre da AWS

    def create_and_deploy_tarfile(self, output_filename, source_dir):
        with tarfile.open(output_filename, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))

        DeployModel().deploy_to_s3(self.model_path + '.tar.gz')


trainProductsClassifier(argv[1] if len(argv) > 1 else 'dev')
