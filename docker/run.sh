#docker pull tensorflow/tensorflow:1.12.0-rc2-devel-py3
#go to local directory of project
#docker run -v $PWD:/tmp --rm  tensorflow/tensorflow:1.12.0-rc2-devel-py3 python3 /tmp/inference.py --im /tmp/images/9_inv_dil.jpg --mo /tmp/ckpt/best_model.hdf5
docker run --rm -v $PWD/ledmatrix:/tmp buster-tflite2:latest --image /tmp/images/4_inv_dil.jpg --model /tmp/ckpt/best_model.tflite
