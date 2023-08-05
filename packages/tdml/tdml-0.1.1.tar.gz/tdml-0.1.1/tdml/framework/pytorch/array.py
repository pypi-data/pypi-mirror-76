import torch

def dtype():
	return {
		'float32': torch.float32,
		'float64': torch.float64,
		'int32': torch.int32,
		'int64': torch.int64
	}

def array(data, dtype=None):
	return torch.tensor(data, dtype=dtype)

def astype(array, dtype):
	return array.type(dtype)

def concatenate(array_list, axis=1):
	return torch.cat(array_list, dim=axis)

def expand_axis(array, axis=1):
	shape = list(array.shape)
	shape.insert(axis, 1)
	return array.view(shape)

def unique(array):
	return torch.unique(array)

def tolist(array):
	return array.tolist()

def shape(array):
	return array.shape

def max(array, axis=0):
	return torch.max(array, axis=axis).values.item()

def index_select(array, idx):
	if len(shape(array)) == 1:
		return array[idx]
	elif len(shape(array)) == 2:
		return array[idx, :]