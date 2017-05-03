from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
import numpy as np
import os, sys
import h5py
from read_label import *

data_path = sys.argv[1]

data = []
label = []
for root, dirs, files in os.walk(data_path):
    for fid in files:
        fn = os.path.join(root, fid)
        d, l = read_label(fn)
        data.extend(d)
        label.extend(l)
        print 'loaded ' + fn

x_train = np.asarray(data)
y_train = np.asarray(label)
x_train.shape = (x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
print x_train.shape

#data, label = read_label(sys.argv[1])
#x_train = np.asarray(data)
#x_train.shape = (x_train.shape[0], x_train.shape[1], x_train.shape[2], 1)
#y_train = np.asarray(label)

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(6, 30, 1)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

checkpointer = ModelCheckpoint(filepath="./models/weights.{epoch:02d}-{val_loss:.2f}.hdf5", verbose=1, save_best_only=True, period=1000)
model.fit(x_train, y_train, batch_size=32, epochs=100000, validation_split=0.2, callbacks=[checkpointer])
