import pandas as pd
import pymongo
import unidecode
import re 
import string
import nltk
import sys
import tensorflow_datasets as tfds
import tensorflow as tf
import pickle
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
import json 
from pathlib import Path
import shutil
import tarfile
import gdown

from nkia.ml.cnn_nlp_model import CNN

def get_dataframe_from_mongo(mongo_conn):
    products_df = mongo_conn.db.df_products.find({}).sort('created', pymongo.DESCENDING)
    
    if products_df:
        return pd.DataFrame(products_df[0]['df'])

    return ''

def get_cleaned_predictor(description, product_name):
    description = list(map(get_description_and_name, description))
    product_name = list(map(get_description_and_name, product_name))

    X = join_all_predictors(description, product_name)

    return X

def get_description_and_name(data):    
    stop_words = nltk.corpus.stopwords.words('portuguese')

    data = unidecode.unidecode(data[0]).lower()
    data = re.sub(r'['+string.punctuation+']', '', data)
    data = [word for word in data.split() if word not in stop_words]
    
    return ' '.join(data)   

def join_all_predictors(description, product_name):
    count = 0
    X = []

    for name in product_name:
        X.append(name + ' ' + description[count])
        count += 1

    return X

def preprocessing_fn(X, token_path):
    X, tokenizer = tokenize_data(X, token_path)
    X = padding_matrix(X)

    print('Preprocessing_fn finished')
    sys.stdout.flush()
    return X, tokenizer

def tokenize_data(data, token_path):
    tokenizer = tfds.features.text.SubwordTextEncoder.build_from_corpus(
        data, target_vocab_size=2**14)

    tokenizer.save_to_file(token_path)
    data = [tokenizer.encode(sentence) for sentence in data]

    return data, tokenizer

def padding_matrix(data):
    max_sentence_len = max([len(sentence) for sentence in data])
    data = tf.keras.preprocessing.sequence.pad_sequences(data,
                                                            value=0,
                                                            padding='post',
                                                            maxlen=max_sentence_len)

    return data

def encode_class_value(class_value, encoder_path):
    encoder = LabelEncoder()
    y = encoder.fit_transform(class_value)

    output_encoder = open(encoder_path, 'wb')
    pickle.dump(encoder, output_encoder)
    output_encoder.close()
    
    return y

def evaluate_model(model, X_test, y_test):
    y_pred_test = model.predict(X_test)
    predicted = [result.argmax() for result in y_pred_test]
    
    f_score = f1_score(y_test, predicted , average='macro')
    accuracy = model.evaluate(X_test, y_test, batch_size=64)[1]

    print(classification_report(y_test, predicted))
    print('Accuracy: ', accuracy)

    return accuracy, f_score

def show_confusion_matrix(y_test, predicted):
    fig, ax = plt.subplots(figsize=(10,10))
    cm = confusion_matrix(y_test, predicted)
    sns.heatmap(cm, annot=True)
    plt.show()

def create_model_instance(y, vocab_size):
    nb_classes = len(set(y))

    cnn = CNN(vocab_size=vocab_size, emb_dim=300, nb_filters=100,
        ffn_units=256, nb_classes=nb_classes, dropout_rate=0.2)

    print('Created model instance')
    sys.stdout.flush()
    return cnn

def create_saved_model_folder(model_name):
    last_model_version = json.loads(read_file(os.getcwd() + '/config.txt'))['version']
    new_model_version = get_new_model_version(last_model_version)

    model_path = os.path.join('./src/nkia/ml/saved_model/' + model_name + '/')
    
    if os.path.exists(model_path + new_model_version):
        shutil.rmtree(model_path + new_model_version)
    os.makedirs(model_path + new_model_version)

    versions_stored = os.listdir(model_path)
    
    # if len(versions_stored) > 1:
    #     versions_stored.remove(new_model_version) 
    #     last_model_path = model_path + versions_stored[0]        
    # else:
    #     get_model_files_by_version(model_path, last_model_version)
    #     last_model_path = model_path + last_model_version        

    model_path = model_path + new_model_version
    return model_path, ''

def read_file(file_name, content=''):
    if content:
        with open(os.path.join(Path(os.path.dirname(__file__)), file_name), 'w') as _file:
            _file.write(str(content))
            _file.close()
    else:
        with open(os.path.join(Path(os.path.dirname(__file__)), file_name)) as _file:
            return _file.read()

def get_new_model_version(last_model_version):
    new_model_version = last_model_version.split('.')
    new_model_version.insert(1, str(int(new_model_version.pop(1)) + 1))
    return '.'.join(new_model_version)

def get_model_files_by_version(model_name, model_version):
    url = 'https://{}.s3.amazonaws.com/{}'.format('category-model', model_version + '.tar.gz')

    if 'category_model' in model_name.split('/'):
        if model_version not in os.listdir(model_name):
            download_model(url, model_name + model_version + '.tar.gz')

    elif 'food_model' in model_name.split('/'):
        if model_version not in os.listdir(model_name):
            download_model(
                'https://drive.google.com/u/1/uc?export=download&confirm=8g0K&id=1cC5i6hplYq3j13plJc3x6BcvmEskC_bp', 'food_model.tar.gz')

def download_model(url, output):
    gdown.download(url, output, quiet=False) 

    tar = tarfile.open(output)
    tar.extractall('/'.join(output.split('/')[0:-1]))
    tar.close()
    os.remove(output)
