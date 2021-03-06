# -*- coding: utf-8 -*-
"""Image_Recognition_CIFAR-10.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13PbzHHdOp9DD6Toqiof57-VkUZwQlGQP
"""

import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np

from keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')

print('y_train shape', y_train.shape)
print(x_test.shape[0], 'test samples')

print('x_test shape', x_test.shape)
print(y_test.shape[0], 'test samples')

# Declare variables
batch_size = 32 
# 32 examples in a mini-batch, smaller batch size means more updates in one epoch
epochs = 100
class_names = ["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]

print(class_names[int(y_train[25416])])
print(range(x_train.shape[0]))
count=0
for e in range(x_train.shape[0]):
 # print(e)
  if class_names[int(y_train[e])]=="airplane":
    count=count+1
print(count)

#Kiíratjuk elsőnek az airplane classba tartozó elemek számát
count1=0
for f in range(x_train.shape[0]):
  if class_names[int(y_train[f])]=="cat":
     count1=count1+1
print(count1)
usedtotrain=[]

percentCount=0
percentCount1=0
for f in range(x_train.shape[0]):
  if class_names[int(y_train[f])]=="cat" or class_names[int(y_train[f])]=="bird" or class_names[int(y_train[f])]=="dog":
    percentCount1=percentCount1+1
    if percentCount%2==0:
    #print("ok")
      usedtotrain.append(f)
  else:
    percentCount=percentCount+1
    if percentCount%50==0: 
      usedtotrain.append(f)


#ellenőrzöm a usetotrain array-emet.
#cnt=0
#print(usedtotrain)
#for t in range(9500):
#  if y_train[usedtotrain][t]==6:
#    cnt=cnt+1

#print(cnt)

x_train=x_train[usedtotrain,:]
y_train=y_train[usedtotrain,:]
#print(x_train.shape)
#print(y_train.shape)

usedtotrain1=[]
cnt1=0
for gj in range(50000):
  cnt1=cnt1+1
  if cnt1%10==0:
    usedtotrain1.append(cnt1-1)
  

#x_train=x_train[usedtotrain1,:]
#y_train=y_train[usedtotrain1,:]
#ellenőrizzük a shape-jét az új módosított x_train és y_train függvényünknek

print(x_train.shape)
print(y_train.shape)

def plot_images(x, y, number_of_images=5):
  fig, axes1 = plt.subplots(number_of_images,number_of_images,figsize=(8,8))
  for j in range(number_of_images):
      for k in range(number_of_images):
          i = np.random.choice(range(len(x)))
          title = class_names[y[i:i+1][0][0]]
          axes1[j][k].title.set_text(title)
          axes1[j][k].set_axis_off()
          axes1[j][k].imshow(x[i:i+1][0])

plot_images(x_train, y_train, number_of_images=9)

model = tf.keras.Sequential()

model.add(tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(32, 32, 3)))
model.add(tf.keras.layers.Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2)))
model.add(tf.keras.layers.Dropout(0.25))

model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(1024, activation='relu'))
model.add(tf.keras.layers.Dropout(0.5))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer=tf.keras.optimizers.Adam(lr=0.0001, decay=1e-6),
              metrics=['accuracy'])

# Train the model
history=model.fit(x_train / 255.0, tf.keras.utils.to_categorical(y_train),
          batch_size=batch_size,
          shuffle=True,
          epochs=epochs,
          validation_data=(x_test / 255.0, tf.keras.utils.to_categorical(y_test))
          )

# Evaluate the model
scores = model.evaluate(x_test / 255.0, tf.keras.utils.to_categorical(y_test))

print('Loss: %.3f' % scores[0])
print('Accuracy: %.3f' % scores[1])

tf.keras.utils.plot_model(
    model, to_file='model.png', show_shapes=False, show_layer_names=True,
    rankdir='TB', expand_nested=False, dpi=96
)
 
print(history.history.keys())
#  "Accuracy"
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
# "Loss"
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()