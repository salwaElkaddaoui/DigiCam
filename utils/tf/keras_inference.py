"""
Inference on a keras model
Path to input image and path to h5 file shoud be given as arguments to this script

Author: Salwa eL KADDAOUI
"""

import sys, os
import argparse, logging

import numpy as np
import tensorflow as tf

def read_image(image_path: str) -> tf.Tensor:
    """Reads an image with tensoflow.
        #Arguments:
            image_path: path to the image to read
        #Returns:
            the image as a tensorflow tensor
    """
    image = tf.image.decode_jpeg( tf.io.read_file( image_path ) )
    image = tf.expand_dims( tf.image.resize_images(image, (28, 28) ), axis=0 )
    image = tf.math.multiply( tf.cast( image, tf.float32 ), 1/255. )
    return image

def parse_arguments() -> argparse.Namespace:
    """Parse script input arguments
        #Arguments:
            None
        #Returns:
            object containing attributes (==arguments)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--im', dest='im', help='image path')
    parser.add_argument('--mo', dest='mo', help='model path')
    args = parser.parse_args()

    if not os.path.exists(args.im):
        raise IOError('Given image path does not exist')
    if not os.path.exists(args.mo):
        raise IOError('Given model path does not exist')

    logging.info('Input Arguments successfully parsed.')
    return args

def main(args):
    """Main function of th Program:
        1. Load model
        2. Read image
        3. Make prediction and print predicted class and confidence
        #Arguments:
            Script parsed arguments
        #Returns:
            None
    """
    model = tf.keras.models.load_model(args.mo, compile = True)
    image = read_image(args.im)
    predictions = model.predict(image, steps=1)
    logging.info("We think it's a {} with a confidence of {:.2f}".format(np.argmax(predictions), max(predictions[0])))

if __name__=='__main__':
    args = parse_arguments()
    main(args)
