import tensorflow as tf
from tensorflow.python.platform import gfile
import sys, cv2
import numpy as np

def read_image(image_path):
    image = tf.image.decode_jpeg( tf.io.read_file( image_path ) )
    image = tf.expand_dims( tf.image.resize_images(image, (28, 28) ), axis=0 )
    image = tf.math.multiply( tf.cast( image, tf.float32 ), 1/255. )
    return image

image_path = 'images/6_inv_dil.jpg'
# x = read_image(image_path)
# x = tf.image.decode_jpeg( tf.io.read_file( image_path ) )
x = np.array( [ np.expand_dims( cv2.resize( cv2.imread(image_path, 0), (28, 28) ), axis=2 ) ] ).astype(np.float32)/255.

with tf.Session() as sess:
    with gfile.FastGFile('ckpt/best_model.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        sess.graph.as_default()
        g_in = tf.import_graph_def(graph_def)

        print('\n\n\n\n')
        print(sess.graph.get_operations())
        print('\n\n\n\n')
        for op in sess.graph.get_operations():
            print(op)
        tensor_input = sess.graph.get_tensor_by_name('import/conv2d_input:0')
        tensor_output = sess.graph.get_tensor_by_name('import/dense/Softmax:0')
        predictions = sess.run(tensor_output, {tensor_input: x})
        print(np.argmax(predictions))
