"""
Conversion of a keras model to a tensorflow lite model
Output tflite model is saved in the same folder as the input keras model
"""
import tensorflow as tf
import os
import argparse

parser = argparse.ArgumentParser(description='Utility for the conversion of keras models to tflite')
parser.add_argument('--mo', dest='mo', help='path to keras model')
args = parser.parse_args()
if not os.path.exists(args.mo):
    raise IOError('Given path to keras model does not exist')

converter = tf.contrib.lite.TFLiteConverter.from_keras_model_file(args.mo)
converter.optimizations = [tf.contrib.lite.ConverterMode.DEFAULT]
tflite_quantized_model = converter.convert()
open(args.mo.replace( os.path.basename(args.mo).split('.')[1], 'tflite' ), "wb").write(tflite_quantized_model)
print('Keras model is successfully converted to tflite.')
