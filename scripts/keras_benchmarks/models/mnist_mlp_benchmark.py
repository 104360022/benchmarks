'''
Original Model from keras/examples

Trains a simple deep NN on the MNIST dataset.
Gets to 98.40% test accuracy after 20 epochs
(there is *a lot* of margin for parameter tuning).
2 seconds per epoch on a K520 GPU.
'''

from __future__ import print_function

import time
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

from model import BenchmarkModel
from models import timehistory

class MnistMlpBenchmark(BenchmarkModel):

    _test_name = "mnist_mlp"
    _sample_type="images"
    _total_time = 0
    _batch_size = 0
    _epochs = 0

    def benchmarkMnistMlp(self):

        self._batch_size = 128
        num_classes = 10
        self._epochs = 20

        # the data, shuffled and split between train and test sets
        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        x_train = x_train.reshape(60000, 784)
        x_test = x_test.reshape(10000, 784)
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255
        print(x_train.shape[0], 'train samples')
        print(x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, num_classes)
        y_test = keras.utils.to_categorical(y_test, num_classes)

        model = Sequential()
        model.add(Dense(512, activation='relu', input_shape=(784,)))
        model.add(Dropout(0.2))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(num_classes, activation='softmax'))

        model.summary()

        model.compile(loss='categorical_crossentropy',
                      optimizer=RMSprop(),
                      metrics=['accuracy'])

        start_time = time.time()
        time_callback = timehistory.TimeHistory()
        history = model.fit(x_train, y_train,
                            batch_size=self._batch_size,
                            epochs=self._epochs,
                            verbose=1,
                            validation_data=(x_test, y_test),
                            callbacks=[time_callback])

        self._total_time = time.time() - start_time - time_callback.times[0]

        score = model.evaluate(x_test, y_test, verbose=0)

        print('Test loss:', score[0])
        print('Test accuracy:', score[1])

    def get_totaltime(self):
        return self._total_time

    def get_iters(self):
        return self._iters

    def get_testname(self):
        return self._test_name

    def get_sampletype(self):
        return self._sample_type

    def get_batch_size(self):
        return self._batch_size
