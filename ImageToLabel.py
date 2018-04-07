import os

import numpy as np
import tensorflow as tf
import utils


class ImageToLabel:
    saver = None
    sess = None

    def __init__(self):
        currentPath = os.path.split(os.path.realpath(__file__))[0]
        self.saver = tf.train.import_meta_graph(
            os.path.join(currentPath, './ckpt/zfjwc_captcha_tensor_data.ckpt-1200.meta'))
        self.sess = tf.Session()
        self.saver.restore(self.sess, os.path.join(currentPath, './ckpt/zfjwc_captcha_tensor_data.ckpt-1200'))

    def getImageLabel(self, imageBytes):
        image = utils.bytesToCv2Image(imageBytes)
        imageArray = utils.getCharArray(image)
        label = ''
        for i in range(4):
            outputLable = self.sess.run('output_label:0', feed_dict={
                'input_image:0': imageArray[i].reshape(1, 22 * 12),
                'input_label:0': np.zeros((1, 36)),
                'keep_prob:0': 1.0
            }
                                        )
            label += utils.ontHotToChar(outputLable[0])
        return label

    def __del__(self):
        self.sess.close()
