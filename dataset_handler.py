import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.text import Tokenizer
#configuration file for data in csv
from model_configurations import configuration

class DatasetSpliter(object):

    def __init__(self,dataset_path,vocab_size,max_length):
        self.data = pd.read_csv(configuration.dataset_path, header = 0, names = ['Query', 'Description'])
        self.split_data()
        self.vocab_size=configuration.vocab_size
        self.max_length=configuration.max_length
        self.split_data()

    def split_data(self):
        # spliting the data as 80% to train and 20% persent to test the data
        train, test = train_test_split(self.data, test_size=0.2)

        self.train_description = train['Description']
        self.train_labels = train['Query']

        self.test_description = test['Description']
        self.test_labels = test['Query']

    def data_encode(self):

        # define Tokenizer with Vocab Size
        tokenizer = Tokenizer(num_words=self.vocab_size)
        tokenizer.fit_on_texts(self.train_descs)
        x_train = tokenizer.texts_to_matrix(self.train_description, mode='tfidf')
        x_test = tokenizer.texts_to_matrix(self.test_desccription, mode='tfidf')

        encoder = LabelBinarizer()
        encoder.fit(self.train_labels)
        y_train = encoder.transform(self.train_labels)
        y_test = encoder.transform(self.test_labels)
        return x_train, y_train, x_test, y_test
