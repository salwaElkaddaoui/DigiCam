#docker pull tensorflow/tensorflow:1.12.0-rc2-devel-py3
#go to local directory of project
docker run -v $PWD:/tmp --rm  tensorflow/tensorflow:1.12.0-rc2-devel-py3 python3 /tmp/inference.py --im /tmp/images/9_inv_dil.jpg --mo /tmp/ckpt/best_model.hdf5
