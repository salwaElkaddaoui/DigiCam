#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Program for reading a tensorflow frozen graph (.pb file) and saving the graph
as tf summaries in a tensorboard logdir:

.pb -> logdir/events.out.tfevents.*** -> tensorboard

Usefulness: by visualizing the graph in tensorboard, you can find the names
of input and output nodes of the graph, which are necessary for making
an inference on a neural network.

"""

from __future__ import unicode_literals
from __future__ import print_function

import os, sys
import argparse, logging

try:
    import tensorflow as tf
except:
    raise ImportError('You need to pip3 install tensorflow.')
from tensorflow.python.platform import gfile


def parse_arguments() -> argparse.Namespace:
    """Parse program input arguments.

        #Arguments:
            None
        #Returns:
            Parsed arguments (an object for storing attributes)
    """
    parser = argparse.ArgumentParser()
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(2)
    parser.add_argument('--graphpath', dest='graph', help='path to frozen graph file (.pb)')
    parser.add_argument('--logdir', dest='log', help='path to logdir')
    args = parser.parse_args()

    if not os.path.exists(args.graph):
        raise ValueError('Given path to frozen graph does not exist.')
    if not os.path.exists(args.log):
        logging.warning('Creating in log folder the current working directory.')
        try:
            os.mkdir(args.log)
        except OSError:
            print('Creation of the directory {} failed.'.format(args.log))
        else:
            print('Successfully created the directory {}.'.format(args.log))

    return args


def main(args: argparse.Namespace) -> None:
    """Main function of the script:
        1. Parse .pb file
        2. Save tensorboard summaries in log folder, so that we can visualize the graph in tensorboard.

        #Arguments:
            Script input arguments
        #Returns:
            None
    """
    with tf.Session() as sess:
        with gfile.FastGFile(args.graph, 'rb') as f: #'ckpt/best_model.pb'
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            sess.graph.as_default()
            g_in = tf.import_graph_def(graph_def)
            writer = tf.summary.FileWriter(args.log)
            writer.add_graph(sess.graph)
            writer.flush()
            writer.close()


if __name__=='__main__':
    args = parse_arguments()
    main(args)
