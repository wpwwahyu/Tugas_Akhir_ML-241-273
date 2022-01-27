# -*- coding: utf-8 -*-
"""Pneumonia Using CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N55z6s8Zj70ooI6Bw4aVMDs1-IHTS9u9
"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# Ubah lokasi direktori kerja
# Sesuaikan dengan path anda
# %cd /content/drive/MyDrive/ml
!ls

data_dir = "/content/drive/MyDrive/xray/chest_xray.zip"

!unzip "/content/drive/MyDrive/xray/chest_xray.zip" -d "/content/drive/MyDrive/ml"

# Cek isi direktori kerja untuk memastikan dataset telah berhasil diekstrak.
!ls

import os
base_dataset = "chest_xray"
class_dir = ['NORMAL', 'PNEUMONIA']
for class_item in class_dir:
  cur_dir = base_dataset+"/"+class_item
  dataset = os.listdir(cur_dir)
  for item in dataset:
    if not item.endswith(".jpeg"):
        os.remove(os.path.join(cur_dir, item))

!pip install split_folders
import splitfolders

#untuk menetapkan directory

input_folder = "/content/drive/MyDrive/ml/chest_xray"
base_dir = "/content/drive/MyDrive/ml/split_folder_ml_pneumonia"

splitfolders.ratio(input_folder, output = base_dir, seed=1337, ratio=(0.80,0.19,0.01))

import os
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'val')
test_dir = os.path.join(base_dir, 'test')

train_normal_dir = os.path.join(train_dir, 'NORMAL')
train_pneumonia_dir = os.path.join(train_dir, 'PNEUMONIA')

validation_normal_dir = os.path.join(validation_dir, 'NORMAL')
validation_pneumonia_dir = os.path.join(validation_dir, 'PNEUMONIA')

test_normal_dir = os.path.join(test_dir, 'NORMAL')
test_pneumonia_dir = os.path.join(test_dir, 'PNEUMONIA')

print('Train NORMAL :', os.listdir(train_normal_dir)[:10])
print('Train PNEUMONIA :', os.listdir(train_pneumonia_dir)[:10])
print("\n")

print('Validation NORMAL :', os.listdir(validation_normal_dir)[:10])
print('Validation PNEUMONIA :', os.listdir(validation_pneumonia_dir)[:10])
print("\n")

print('Test NORMAL :', os.listdir(test_normal_dir)[:10])
print('Test PNEUMONIA :', os.listdir(test_pneumonia_dir)[:10])

# Commented out IPython magic to ensure Python compatibility.
# Tampilkan 8 image per kelas dengan ukuran 4x4 

# %matplotlib inline

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

nrows = 2
ncols = 4

pic_index = 0

fig = plt.gcf()
fig.set_size_inches( ncols * 4,nrows * 4)

pic_index += 8

train_normal = [os.path.join(train_normal_dir, fname) 
                for fname in os.listdir(train_normal_dir)[pic_index-4:pic_index]]

train_pneumonia = [os.path.join(train_pneumonia_dir, fname) 
                for fname in os.listdir(train_pneumonia_dir)[pic_index-4:pic_index]]

for i, img_path in enumerate(train_normal+train_pneumonia):
    
  # Set up subplot; subplot indices start at 1
  sp = plt.subplot(nrows, ncols, i + 1)
  sp.axis('Off') # Don't show axes (or gridlines)

  img = mpimg.imread(img_path)
  plt.imshow(img)
  plt.title(img_path.split(os.path.sep)[-2])

plt.show()

print('Train NORMAL :', len(os.listdir(train_normal_dir)))
print('Train PNEUMONIA :', len(os.listdir(train_pneumonia_dir)))
print("\n")

print('Validation NORMAL :', len(os.listdir(validation_normal_dir)))
print('Validation PNEUMONIA :', len(os.listdir(validation_pneumonia_dir)))
print("\n")

print('Test NORMAL :', len(os.listdir(test_normal_dir)))
print('Test PNEUMONIA :', len(os.listdir(test_pneumonia_dir)))

# Commented out IPython magic to ensure Python compatibility.
import matplotlib.pyplot as plt 
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from keras.callbacks import ReduceLROnPlateau

# import library to build our model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dropout, Flatten, Dense, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import Model
#from tensorflow.keras.applications.vgg16 import preprocess_input

# plotting
# %matplotlib inline
import matplotlib.image as mpimg
import numpy as np

height = 200
width = 200
batch_size = 32

generator_datagen = ImageDataGenerator(
    rescale = 1./255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

val_gen = ImageDataGenerator(rescale = 1./255)

train_generator = generator_datagen.flow_from_directory(
    train_dir,
    target_size=(height, width),
    class_mode='binary',
    color_mode="rgb",
    shuffle=True,
    batch_size=batch_size
)

validation_generator = val_gen.flow_from_directory(
    validation_dir,
    target_size=(height,width),
    class_mode='binary',
    color_mode="rgb",
    shuffle=False,
    batch_size=batch_size
)

test_generator = val_gen.flow_from_directory(
    test_dir,
    target_size=(height,width),
    class_mode='binary',
    color_mode="rgb",
    shuffle=False,
    batch_size=batch_size
)

import cv2
import numpy as np

# Gather data train
train_data = []
train_label = []
for r, d, f in os.walk(train_dir):
    for file in f:
        if ".jpeg" in file:
            imagePath = os.path.join(r, file)
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (200,200))
            train_data.append(image)
            label = imagePath.split(os.path.sep)[-2]
            train_label.append(label)

train_data = np.array(train_data)
train_label = np.array(train_label)

# Gather data validation
val_data = []
val_label = []
for r, d, f in os.walk(validation_dir):
    for file in f:
        if ".jpeg" in file:
            imagePath = os.path.join(r, file)
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (200,200))
            val_data.append(image)
            label = imagePath.split(os.path.sep)[-2]
            val_label.append(label)

val_data = np.array(val_data)
val_label = np.array(val_label)

# Gather data test
test_data = []
test_label = []
for r, d, f in os.walk(test_dir):
    for file in f:
        if ".jpeg" in file:
            imagePath = os.path.join(r, file)
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (200,200))
            test_data.append(image)
            label = imagePath.split(os.path.sep)[-2]
            test_label.append(label)

test_data = np.array(test_data)
test_label = np.array(test_label)

# Tampilkan shape dari data train dan data validation
print("Train Data = ", train_data.shape)
print("Train Label = ", train_label.shape)
print("Validation Data = ", val_data.shape)
print("Validation Label = ", val_label.shape)
print("Test Data = ", test_data.shape)
print("Test Label = ", test_label.shape)

# Normalisasi dataset
print("Data sebelum di-normalisasi ", train_data[0][0][0])

x_train = train_data.astype('float32') / 255.0
x_test = test_data.astype('float32') / 255.0
x_val = val_data.astype('float32') / 255.0
print("Data setelah di-normalisasi ", x_train[0][0][0])

# Transformasi label encoder
from sklearn.preprocessing import LabelEncoder

print("Label sebelum di-encoder ", train_label[1200:1203])
print("Label sebelum di-encoder ", train_label[2343:2346])

lb = LabelEncoder()
y_train = lb.fit_transform(train_label)
y_test = lb.fit_transform(test_label)
y_val = lb.fit_transform(val_label)

print("Label setelah di-encoder ", y_train[1200:1203])
print("Label setelah di-encoder ", y_train[2343:2346])

x_train.shape

x_val.shape

x_test.shape

from tensorflow.keras import layers
from tensorflow.keras import Model
from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import InputLayer, Dense, Dropout, Conv2D, MaxPool2D, MaxPooling2D, GlobalMaxPooling2D, AveragePooling2D, GlobalAveragePooling2D, Flatten, BatchNormalization

DESIRED_ACCURACY = 0.95

class myCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epochs, logs={}) :
        if(logs.get('acc') is not None and logs.get('acc') >= DESIRED_ACCURACY) :
            print('\nReached 95% accuracy so cancelling training!')
            self.model.stop_training = True

callbacks = myCallback()

"""##Model 1"""

# DEFINISIKAN MODEL ANDA DISINI
model = Sequential()

model.add(InputLayer(input_shape=[200,200,3]))

model.add(Conv2D(filters=128, kernel_size=3, strides=1, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=2, padding='same'))

model.add(Conv2D(filters=64, kernel_size=3, strides=1, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=2, padding='same'))

model.add(Conv2D(filters=32, kernel_size=3, strides=1, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=2, padding='same'))

model.add(Conv2D(filters=16, kernel_size=3, strides=1, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=2, padding='same'))

model.add(Conv2D(filters=16, kernel_size=3, strides=1, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(MaxPool2D(pool_size=2, padding='same'))

model.add(Dropout(0.25))

model.add(Flatten())

# Fully Connected Layer
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

print(model.summary())

from tensorflow.keras.optimizers import Adam

# Compile model
model.compile(loss='binary_crossentropy',
              optimizer=Adam(learning_rate=0.001),
              metrics=['acc'])

history = model.fit(x_train, y_train, batch_size=32, epochs=50, validation_data=(x_test, y_test))

# Commented out IPython magic to ensure Python compatibility.
# summarize history for accuracy
# %matplotlib inline

import matplotlib.pyplot as plt

plt.figure(figsize = (10,7))
plt.xticks(fontsize='15')
plt.yticks(fontsize='15') 
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy', fontsize=15)
plt.ylabel('accuracy', fontsize=15)
plt.xlabel('epoch', fontsize=15)
plt.legend(['train', 'validation'], loc='upper left', fontsize=15)
plt.show()

plt.figure(figsize = (10,8))
plt.xticks(fontsize='15')
plt.yticks(fontsize='15') 
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model Loss', fontsize=15)
plt.ylabel('loss', fontsize=15)
plt.xlabel('epoch', fontsize=15)
plt.legend(['train', 'validation'], loc='upper left', fontsize=15)
plt.show()

model.save('/content/drive/MyDrive/Pneumonia Dataset/Model/BatchNormModelCNNv2.h5')
model.save('/content/drive/MyDrive/Pneumonia Dataset/Model/DropoutModelCNNv2.h5')

from sklearn.metrics import classification_report

from keras.models import load_model

# load model pertama
target_dir = '/content/drive/MyDrive/Pneumonia Dataset/Model'
model_saved = load_model(target_dir + '/BatchNormModelCNN.h5')

target_names = []
for key in train_generator.class_indices:
    target_names.append(key)
print(target_names)

from sklearn.metrics import classification_report

predictions = model.predict(x_test)
predictions = np.round(predictions).astype(int)

print(classification_report(y_test, predictions))

def plot_confusion_matrix(cm, classes, normalize=True, title='Confusion matrix', cmap=plt.cm.Blues):

    """

    This function prints and plots the confusion matrix.

    Normalization can be applied by setting `normalize=True`.

    """

    plt.figure(figsize=(10,10))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()

    tick_marks = np.arange(len(classes))

    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm = np.around(cm, decimals=2)
        cm[np.isnan(cm)] = 0.0
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    thresh = cm.max() / 2.
    
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

target_names = []

for key in train_generator.class_indices:
    target_names.append(key)

from sklearn.metrics import  confusion_matrix
import itertools

pred = model.predict(test_generator)
labels = np.argmax(pred, axis=1)

print('Confusion Matrix')
cm = confusion_matrix(test_generator.classes, labels)
plot_confusion_matrix(cm, target_names, title='Confusion Matrix')

# Commented out IPython magic to ensure Python compatibility.
# summarize history for accuracy
# %matplotlib inline

import matplotlib.pyplot as plt

plt.figure(figsize = (10,7))
plt.xticks(fontsize='15')
plt.yticks(fontsize='15') 
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model Accuracy', fontsize=15)
plt.ylabel('accuracy', fontsize=15)
plt.xlabel('epoch', fontsize=15)
plt.legend(['train'], loc='upper left', fontsize=15)
plt.show()