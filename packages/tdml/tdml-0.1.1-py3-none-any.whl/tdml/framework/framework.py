def dtype() -> dict:
	"""
	Get a dictionary of data types of specified ML framework.

	Returns:
		Data types of specified ML framework. Currently it includes `float32`, `float64`, `int32` and `int64`.
	"""
	pass

def array(data, dtype=None):
	"""
	Get an array-like data for specified ML framework.

	Args:
		data (list): Array-like data.
		dtype: The data type of specified ML framework.

	Returns:
		An array-like data for specified framework.
	"""
	pass

def astype(array, dtype):
	"""
	Convert an array to specified data type.

	Args:
		array: Data array.
		dtype: The data type of specified ML framework.

	Returns:
		An array with specified data type.
	"""
	pass

def concatenate(array_list, axis=1):
	"""
	Concatenate a list of arrays with specified axis.

	Args:
		array_list (list): A list of data arrays.
		axis (int): The axis of concatenation. The default value is 1.

	Returns:
		An array after concatenation.
	"""
	pass

def expand_axis(array, axis=1):
	"""
	Add one dimension to an array.

	Args:
		array: Data array.
		axis (int): The axis of dimension expanding. The default value is 1.

	Returns:
		An array after expanding.
	"""
	pass

def unique(array):
	"""
	Get unique values of an array.

	Args:
		array: Data array.

	Returns:
		An array of unique values.
	"""
	pass

def tolist(array) -> list:
	"""
	Convert an array to a list.

	Args:
		array: Data array.

	Returns:
		List of values from an array.
	"""
	pass

def shape(array) -> tuple:
	"""
	Get the shape of an array.

	Args:
		array: Data array.

	Returns:
		tuple: The shape of array in tuple.
	"""
	pass

def max(array, axis=0):
	"""
	Get the maximum value of an array along specified axis.

	Args:
		array: Data array.
		axis (int): The axis to get the maximum value. The default value is 0.

	Returns:
		The maximum value of an array along specified axis.
	"""
	pass

def index_select(array, idx):
	"""
	Get parts of an array with specified indices.

	Args:
		array: Data array.
		idx: The indices of the parts wanted to be extracted.

	Returns:
		The parts of an array with specified indices.
	"""
	pass