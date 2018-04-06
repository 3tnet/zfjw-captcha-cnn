import tensorflow as tf

import utils

x = tf.placeholder(tf.float32, shape=[None, 22 * 12], name='input_image')
y_ = tf.placeholder(tf.float32, shape=[None, 36], name='input_label')

def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev = 0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)

def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

W_conv1 = weight_variable([5, 5, 1, 32]) # 32为输出通道数目 也可以理解为使用的卷积核个数、得到的特征图张数
b_conv1 = bias_variable([32])

x_image = tf.reshape(x,[-1, 22, 12, 1])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

W_fc1 = weight_variable([11 * 6 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_conv2, [-1, 11 * 6 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32, name='keep_prob')
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 36])
b_fc2 = bias_variable([36])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2, name='output_label')

cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

saver = tf.train.Saver(max_to_keep=1)

images, labels = utils.loadAllData()
with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  for i in range(1200):
    imageBatch, labelBatch = utils.nextTrainDataBatch(50, images, labels, i)
    sess.run(train_step, feed_dict={x: imageBatch, y_: labelBatch, keep_prob: 0.5})
    if (i % 100 == 0):
      train_accuracy = accuracy.eval(feed_dict={
          x: imageBatch, y_: labelBatch, keep_prob: 1.0})
      print("step %d, training accuracy %g"%(i, train_accuracy))
  saver.save(sess, './ckpt/zfjwc_captcha_tensor_data.ckpt', global_step = i + 1)
