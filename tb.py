import tensorflow as tf
from tensorflow.python.platform import gfile
with tf.Session() as sess:
    with gfile.FastGFile('ckpt/best_model.pb', 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        sess.graph.as_default()
        g_in = tf.import_graph_def(graph_def)
        writer = tf.summary.FileWriter('log/')
        writer.add_graph(sess.graph)
        writer.flush()
        writer.close()
        
