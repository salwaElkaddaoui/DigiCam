"""
Inference on a frozen graph file. Names of input and output nodes are specific to this model
"""
import os
import logging, argparse

import tensorflow as tf
from tensorflow.python.platform import gfile
import matplotlib.image as mpimg
import numpy as np

def rgb2gray(img):
    """Converts RGB image to grayscale image.
         #Arguments:
            img: numpy array of shape (*,*,3)
        #Returns:
            img_gray: numpy array of shape (*,*)
    """
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    img_gray = R * 299. / 1000 + G * 587. / 1000 + B * 114. / 1000
    return img_gray

def parse_arguments():
    """Parse script input arguments.
        #Arguments:
            None
        #Returns:
            argparse object that contains arguments as attributes (argparse.Namespace)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', dest='im', help='image path')
    parser.add_argument('--model', dest='mo', help='path to frozen graph file')
    parser.add_argument('--inputTensot', dest='inTen', help='Name of input tensor')
    parser.add_argument('--outputTensor', dest='outTen', help='Name of output tensor')
    args = parser.parse_args()
    if not os.path.exists(args.im):
        raise IOError('Given image path does not exist')
    if not os.path.exists(args.mo):
        raise IOError('Given frozen graph file does not exist')
    return args

def main(args) -> None:
    """Main function of the script
        #Arguments:
            args: argparse.Namespace object
        #Returns:
            None
    """
    x = np.array( [ np.expand_dims( rgb2gray(mpimg.imread(args.im)), axis=2 ) ] ).astype(np.float32)/255.
    with tf.Session() as sess:
        with gfile.FastGFile(args.mo, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            sess.graph.as_default()
            g_in = tf.import_graph_def(graph_def)
            tensor_input = sess.graph.get_tensor_by_name(args.inTen) #'import/conv2d_input:0'
            tensor_output = sess.graph.get_tensor_by_name(args.outTen) #'import/dense/Softmax:0'
            predictions = sess.run(tensor_output, {tensor_input: x})
            logging.info(np.argmax(predictions))

if __name__=='__main__':
    args = parse_arguments()
    main(args)
