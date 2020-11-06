# -*- coding: utf-8 -*-
"""2020.05.01_Convolutional_Neural_Network.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y56mgjPEgHPbMGSy_hWj7k32CDT6cr38
"""

# Commented out IPython magic to ensure Python compatibility.
# %tensorflow_version 1.x

import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random
from tensorflow.examples.tutorials.mnist import input_data as data

batch_length = 32  # batches of 32 images are processed and averaged out
size = [28, 28, 1]  # the size of the image
num_iteration = 1500
info_freq = 100
eval_freq = 1000
num_classes = 10  # the number of possible output classes
learning_rate = 1e-4
num_kernels = [32, 64, 128]  # a list that defines the number of layers and convolutions for our network

tf.reset_default_graph()

# loading MNIST data and preprocessing
mnist_data = data.read_data_sets('/MNIST_data', one_hot=True)

# show an image just to get a sense of what we are dealing with here
img = np.reshape(mnist_data.train.images[4, :], [28, 28])
print(mnist_data.train.images.shape)
plt.imshow(img, cmap="Greys")
plt.show()

# defining arrays for our plots
loss_plot = np.zeros(num_iteration)
acc_plot = np.zeros(num_iteration)

input_data = tf.placeholder(tf.float32, [None] + size)  # input images

one_hot_labels = tf.placeholder(tf.float32, [None, num_classes])  # labels, the expected outputs
keep_prob=tf.placeholder_with_default(
    1.0,
    [],
    name='keep_prob'
)
current_input = input_data
current_filters = size[2]
layer_num = 0

# a loop to create all our layers
for num in num_kernels:
    with tf.variable_scope('conv' + str(layer_num)):
        layer_num += 1

        # variables we want to optimize
        w = tf.get_variable('w', [3, 3, current_filters, num])
        bias = tf.get_variable('bias', [num], initializer=tf.constant_initializer(0.0))

        # convolution
        conv_result = tf.nn.conv2d(current_input, w, strides=[1, 1, 1, 1], padding='VALID')
        current_filters = num

        # we add a bias
        conv_result = tf.add(conv_result, bias)

        relu = tf.nn.relu(conv_result)

        # pooling
        pooled = tf.nn.max_pool(relu, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='VALID')
        current_input = pooled

# we have generated feature maps; we will now use a fully connected layer with 10 neurons, one for each class
# the response of these neurons will represent how strongly the input belongs to the corresponding class
with tf.variable_scope('fully_connected'):
    current_shape = current_input.get_shape()
    
    current_input = tf.layers.batch_normalization(current_input)
    update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
    
    feature_length = int(current_shape[1] * current_shape[2] * current_shape[3])
    fully_connected = tf.reshape(current_input, [-1, feature_length])
    
    fully_connected = tf.nn.dropout(fully_connected,keep_prob=keep_prob)
    
    #dense = tf.matmul(dropped,W)+b
    w = tf.get_variable('w', [feature_length, num_classes])
    fully_connected = tf.matmul(fully_connected, w)
    bias = tf.get_variable('bias', [num_classes])
    fully_connected = tf.add(fully_connected, bias)

  ##?  is_train = tf.placeholder(tf.bool, name="is_train");
  #  print(fully_connected[1][0])
   # x_norm = tf.layers.batch_normalization(fully_connected)
    #print('Batch_Normalization...')
     #update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)

with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.losses.softmax_cross_entropy(one_hot_labels, fully_connected))

with tf.name_scope('optimizer'):
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(loss)

with tf.name_scope('accuracy'): ##itt miért hoz létre új namescopeokat miért nem csak a variable scope-ba
    correct_predictions = tf.equal(tf.argmax(fully_connected, 1), tf.argmax(one_hot_labels, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.float32)) ##reduce mean miért kell a correct pr
 
    init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    step = 0
    print('\nStarting training...\n')

    while step < num_iteration:
        used_in_batch= random.sample(range(mnist_data.train.images.shape[0]), batch_length)
        batch_xs = mnist_data.train.images[used_in_batch,:] 
        batch_ys = mnist_data.train.labels[used_in_batch,:]
        batch_xs = np.reshape(batch_xs,[batch_length]+size) #itt a + size imt jelent?
      
        _, acc, lo = sess.run([optimizer, accuracy, loss], feed_dict={input_data: batch_xs, one_hot_labels: batch_ys})
        loss_plot[step] = lo
        acc_plot[step] = acc * 100

        step += 1

        if step % info_freq == 0:
            print('Step: ' + str(step) + ' Loss: ' + str(lo) + ' Accuracy: ' + str(acc))
        
       
            #test_acc = sum_acc / mnist_data.test.images.shape[0]

            #print('\nAccuracy on independent test set at step ' + str(step) + ': ' + str(test_acc) + '\n')
    
            
    plt.figure()
    plt.plot(loss_plot, 'm')
    plt.xlabel('Training iterations')
    plt.ylabel('Loss')

    plt.figure()
    plt.plot(acc_plot, 'b')
    plt.xlabel('Training iterations')
    plt.ylabel('Accuracy')

    plt.show()
    
    print('Training finished!\n')
    print('Running on independent test set...')
    
    sum_acc = 0.0
    milacc= 0.0
    for i in range(0,mnist_data.test.images.shape[0]):
        batch_xs = mnist_data.test.images[i,:]
        batch_ys = mnist_data.test.labels[i,:]
        batch_xs = np.reshape(batch_xs,[1] + size)
        batch_ys = np.reshape(batch_ys,[1, num_classes])
        
        acc = sess.run(accuracy, feed_dict={input_data: batch_xs, one_hot_labels: batch_ys })
        #acc_plott[i] = acc
        milacc=milacc+acc
        if(i%1000==0):
          
          print(milacc/1000)
          milacc=0
          #print("Test accuracy"+str(acc*100))
        sum_acc += acc
  

    test_acc = sum_acc / mnist_data.test.images.shape[0]
    print('Accuracy on independent test set: ' + str(test_acc))
    
    test_index = random.sample(range(mnist_data.test.images.shape[0]), 1)
    test_image = np.reshape(mnist_data.test.images[test_index, :], (1, 28, 28, 1))
    test_label = mnist_data.test.labels[test_index, :]
    
    # show the image
    img = np.reshape(test_image, [28, 28])
    plt.imshow(img, cmap="Greys")
    plt.show()
    
    print('Label: ', test_label)
    result = sess.run(fully_connected, feed_dict={input_data: test_image, one_hot_labels: test_label})
    print('Network output: ', result)
    print('Label vs. predicition: ', np.argmax(test_label), ',', np.argmax(result))

with tf.Session() as sess:  
    sess.run(init)
    step = 0
    print('\nStarting training...\n')

    while step < num_iteration:
        used_in_batch= random.sample(range(mnist_data.train.images.shape[0]), batch_length)
        batch_xs = mnist_data.train.images[used_in_batch,:]
        batch_ys = mnist_data.train.labels[used_in_batch,:]
        batch_xs = np.reshape(batch_xs,[batch_length]+size) 
      
        _, acc, lo = sess.run([optimizer, accuracy, loss], feed_dict={input_data: batch_xs, one_hot_labels: batch_ys, keep_prob: 0.2})
        loss_plot[step] = lo
        acc_plot[step] = acc * 100

        step += 1

        if step % info_freq == 0:
            print('Step: ' + str(step) + ' Loss: ' + str(lo) + ' Accuracy: ' + str(acc))

plt.figure()
plt.plot(loss_plot, 'm')
plt.xlabel('Training iterations')
plt.ylabel('Loss')

plt.figure()
plt.plot(acc_plot, 'b')
plt.xlabel('Training iterations')
plt.ylabel('Accuracy')

plt.show()

 
       
            #test_acc = sum_acc / mnist_data.test.images.shape[0]

            #print('\nAccuracy on independent test set at step ' + str(step) + ': ' + str(test_acc) + '\n')