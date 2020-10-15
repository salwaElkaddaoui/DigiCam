import tensorflow as tf
from tensorflow.python.platform import gfile
import matplotlib.image as mpimg
import numpy as np
import argparse

def rgb2gray(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    img_gray = R * 299. / 1000 + G * 587. / 1000 + B * 114. / 1000
    return img_gray

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--im', dest='im', help='image path')
parser.add_argument('--mo', dest='mo', help='path to frozen graph file')
args = parser.parse_args()
if not os.path.exists(args.im):
    raise IOError('Given image path does not exist')
if not os.path.exists(args.mo):
    raise IOError('Given frozen graph file does not exist')


x = np.array( [ np.expand_dims( rgb2gray(mpimg.imread(args.im)), axis=2 ) ] ).astype(np.float32)/255.
with tf.Session() as sess:
    with gfile.FastGFile(args.mo, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        sess.graph.as_default()
        g_in = tf.import_graph_def(graph_def)
        tensor_input = sess.graph.get_tensor_by_name('import/conv2d_input:0')
        tensor_output = sess.graph.get_tensor_by_name('import/dense/Softmax:0')
        predictions = sess.run(tensor_output, {tensor_input: x})
        print(np.argmax(predictions))
