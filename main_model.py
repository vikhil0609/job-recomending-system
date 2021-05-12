from tensorflow import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras import metrics
from sklearn.preprocessing import LabelBinarizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import one_hot
from model_configurations import configuration
from dataset_handler import DatasetSpliter


class Main_Model(object):
    def __init__(self):
        spliter=DatasetSpliter()
        split_data=spliter.data_encode()

        self.x_train=split_data[0]
        self.y_train = split_data[1]
        self.x_test = split_data[2]
        self.y_test = split_data[3]
        self.test_labels=spliter.test_labels

        self.create_model()

    def create_model(self):
        self.model = Sequential()
        self.model.add(Dense(configuration.dense, input_shape=(configuration.vocab_size,)))
        self.model.add(Activation(configuration.activation_function))
        self.model.add(Dropout(configuration.dropout))
        self.model.add(Dense(configuration.dense))
        self.model.add(Activation(configuration.activation_function))
        self.model.add(Dropout(configuration.dropout))
        self.model.add(Dense(configuration.labels))
        self.model.add(Activation(configuration.last_activation_function))

        #Compile the model
        self.compile_model()

    def compile_model(self):
        self.model.compile(loss = configuration.loss,
                           optimizer = configuration.optimizer,
                           metrics = [metrics.categorical_accuracy, 'accuracy'])

        print(self.model.summary())
        self.create_history()
    def create_history(self):
        '''early_stopping_patience = 10
        # Add early stopping
        early_stopping = keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=early_stopping_patience, restore_best_weights=True)
'''

        self.model.fit(self.x_train, self.y_train,
                            batch_size=configuration.batch_size,
                            epochs=configuration.nb_epoch,
                            verbose=configuration.verbose,
                            validation_split=configuration.validation_split,
                            #callbacks=[early_stopping],
                            )

        Accuracy = self.model.evaluate(self.x_test, self.y_test,
                               batch_size=configuration.batch_size, verbose=1)

        print('Accuracy:', Accuracy[2])


    def prediction(self,user_text):

        # Encode the text
        encoded_docs = [one_hot(user_text, configuration.vocab_size)]
        # pad documents to a max length
        padded_text = pad_sequences(encoded_docs, maxlen=configuration.max_length, padding='post')
        # Prediction based on model
        prediction = self.model.predict(padded_text)
        # Decode the prediction
        encoder = LabelBinarizer()
        encoder.fit(self.test_labels)
        result = encoder.inverse_transform(prediction)
        return result[0]
