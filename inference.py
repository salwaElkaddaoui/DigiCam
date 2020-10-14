import sys, os
import tensorflow as tf
import numpy as np
import argparse

def read_image(image_path):
    image = tf.image.decode_jpeg( tf.io.read_file( image_path ) )
    image = tf.expand_dims( tf.image.resize(image, (28, 28) ), axis=0 )
    image = tf.math.multiply( tf.cast( image, tf.float32 ), 1/255. )
    return image

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--im', dest='im', help='image path')
args = parser.parse_args()

if not os.path.exists(args.im):
    raise IOError('Given image path does not exists')

model = tf.keras.models.load_model('ckpt/best_model.hdf5', compile = True)
image = read_image(args.im)
predictions = model.predict(image, steps=1)
print("We think it's a {} with a confidence of {:.2f}".format(np.argmax(predictions), max(predictions[0])))
