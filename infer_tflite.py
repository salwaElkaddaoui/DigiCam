"""
Makes an inference on a tflite model.
based on: https://github.com/tensorflow/examples/blob/master/lite/examples/image_classification/raspberry_pi/classify_picamera.py
"""
import os
import numpy as np
from PIL import Image
import argparse
from tflite_runtime.interpreter import Interpreter

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
  """Returns a sorted array of classification results."""
  set_input_tensor(interpreter, image)
  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  # If the model is quantized (uint8 data), then dequantize the results
  if output_details['dtype'] == np.uint8:
    scale, zero_point = output_details['quantization']
    output = scale * (output - zero_point)

  ordered = np.argpartition(-output, top_k)
  return [(i, output[i]) for i in ordered[:top_k]]


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

def main():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    parser.add_argument('--model', help='File path of .tflite file.', required=True)
    parser.add_argument('--image', help='File path to input image.', required=True)
    args = parser.parse_args()

    if not os.path.exists(args.image):
        raise IOError('Given path to image does not exist.')

    image = rgb2gray( np.expand_dims(np.asarray( Image.open(args.image).convert("RGB").resize((28,28)) ), axis=2) )

    interpreter = Interpreter(args.model)
    interpreter.allocate_tensors()
    _, height, width, _ = interpreter.get_input_details()[0]['shape']

    results = classify_image(interpreter, image)
    label_id, prob = results[0]
    print('That\'s a {}, we\'re {:.2f}% sure of that'.format(label_id, prob*100))

if __name__=='__main__':
    main()
