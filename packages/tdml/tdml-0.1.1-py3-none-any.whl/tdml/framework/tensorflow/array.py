import numpy as np
import tensorflow as tf

def dtype():
	return {
		'float32': tf.float32,
		'float64': tf.float64,
		'int32': tf.int32,
		'int64': tf.int64
	}

def array(data, dtype=None):
	return tf.constant(data, dtype=dtype)

def astype(array, dtype):
	return tf.cast(array, dtype)

def concatenate(array_list, axis=1):
	return tf.concat(array_list, axis=axis)

def expand_axis(array, axis=1):
	return tf.expand_dims(array, axis=axis)

def unique(array):
	return tf.sort(tf.unique(array)[0])

def tolist(array):
	return array.numpy().tolist()

def shape(array):
	return array.shape.as_list()

def max(array, axis=0):
	res = tf.math.reduce_max(array, axis=axis)
	if len(res.shape.as_list()) == 0:
		return res.numpy()
	return res

def index_select(array, idx):
	if isinstance(idx, np.ndarray):
		if len(idx.shape) == 1 or len(idx.shape) == 2:
			idx = idx.reshape(len(idx), 1)
		return tf.gather_nd(array, idx)