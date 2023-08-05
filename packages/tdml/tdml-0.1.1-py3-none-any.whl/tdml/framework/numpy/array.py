import numpy as np

def dtype():
	return {
		'float32': np.float32,
		'float64': np.float64,
		'int32': np.int32,
		'int64': np.int64
	}

def array(data, dtype=None):
	return np.array(data, dtype=dtype)

def astype(array, dtype):
	return array.astype(dtype)

def concatenate(array_list, axis=1):
	return np.concatenate(array_list, axis=axis)

def expand_axis(array, axis=1):
	return np.expand_dims(array, axis=axis)

def unique(array):
	return np.unique(array)

def tolist(array):
	return array.tolist()

def shape(array):
	return array.shape

def max(array, axis=0):
	return np.max(array, axis=axis)

def index_select(array, idx):
	if len(shape(array)) == 1:
		return array[idx]
	elif len(shape(array)) == 2:
		return array[idx, :]