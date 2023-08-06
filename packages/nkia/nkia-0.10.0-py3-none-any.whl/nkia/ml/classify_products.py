import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

import tensorflow_datasets as tfds
import pickle
import numpy as np

import utils.utils as utils
from nkia.ml.cnn_nlp_model import CNN
import pkg_resources

class classifyProducts(object):

    def __init__(self):
        self.utils = utils
        self.load_model_to_memory('category_model')

    def load_model_to_memory(self, model_name):
        model_version = pkg_resources.get_distribution('nkia').version

        os.makedirs(model_name) if model_name not in os.listdir() else ...
        self.utils.get_model_files_by_version(model_name + '/', model_version)

        self.tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(
            './'+model_name+'/'+model_version+'/token')

        nb_classes = 29 if model_name == 'category_model' else 2

        cnn = CNN(vocab_size=self.tokenizer.vocab_size, emb_dim=300, nb_filters=100,
            ffn_units=256, nb_classes=nb_classes, dropout_rate=0.2)

        cnn.load_weights('./'+model_name+'/'+model_version+'/model_checkpoint/cp.ckpt').expect_partial()
        return cnn

    def inference_from_category_model(self, model, product_name=[''], description=['']): 
        """
        This method is responsible to infer the product category based on your caracteristics. Pass just one product
        by time.

        Args:
            product_name (list):  ['energético sabor baunilha']
            description (list):  ['Esse produto é simplesmente fantástico']

        Returns:
            str: Category name. e.g: 'Bebidas não alcoolicas'

        """     
        model_version = pkg_resources.get_distribution('nkia').version

        X = self.utils.get_cleaned_predictor([description], [product_name])
        X = self.preprocessing_fn(X, './category_model'+'/'+model_version+'/token')

        label_encoder = self.get_label_encoder('./category_model'+'/'+model_version+'/label_encoder.pkl')

        product_category = model(np.array(X), training=False).numpy()[0]

        product_category_proba = product_category[product_category.argmax()]

        if product_category_proba < 0.6:
            product_category = 'categoria desconhecida'
        else:
            product_category = label_encoder.inverse_transform([product_category.argmax()])[0]

        return product_category

    def inference_from_food_model(self, model, product_name):
        """
        This method is responsible to infer if a product is a food or not. Pass just one product
        by time.

        Args:
            product_name (list):  ['energético sabor baunilha']

        Returns:
            str: food or not food.

        """     
        X = self.utils.get_description_and_name(product_name)
        X = self.preprocessing_fn([X], './food_model/v1/token')

        label_encoder = self.get_label_encoder('./food_model/v1/label_encoder.pkl')

        product_type = model(np.array(X), training=False).numpy()
        product_type = 1 if product_type > 0.5 else 0

        return label_encoder.inverse_transform([product_type])[0] 

    def preprocessing_fn(self, X, token_path):
        self.tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file(token_path)
        tokenized_predictor = [self.tokenizer.encode(sentence) for sentence in  X] 

        return tokenized_predictor

    def get_label_encoder(self, encoder_path):
        pkl_encoder_file = open(encoder_path, 'rb')
        encoder = pickle.load(pkl_encoder_file) 
        pkl_encoder_file.close()
        return encoder

classifyProducts()