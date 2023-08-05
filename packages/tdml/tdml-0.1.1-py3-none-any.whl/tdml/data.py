from . import framework as arr

class Data():
	"""
	The data class of TDML.
	"""
	def __init__(self, data):
		self.data = data

	@property
	def shape(self):
		"""
		The shape of the data.
		"""
		return arr.shape(self.data)

	@property
	def num_sample(self):
		"""
		The number of samples in the dataset.
		"""
		return arr.shape(self.data)[0]

	def reshuffle(self, reshuffle_indices):
		"""
		Reshuffle the data with specified indices.

		Args:
			reshuffle_indices: The pre-specified indices in :class:`numpy.ndarray`.
		"""
		self.data = arr.index_select(self.data, reshuffle_indices)

	def __str__(self):
		string = 'Data(data={})'
		string = string.format(list(arr.shape(self.data)))
		return string

class Feature(Data):
	"""
	The feature data class inherited from the :class:`tdml.data.Data`.
	"""
	def __init__(self, data):
		self.data = data

	@property
	def num_feature(self):
		"""
		The dimension of the data features.
		"""
		return arr.shape(self.data)[1]

class Label(Data):
	"""
	The label data class inherited from the :class:`tdml.data.Data`.
	"""
	def __init__(self, data):
		self.data = data

	@property
	def num_label(self):
		"""
		The number of labels.
		"""
		return arr.max(self.data, axis=0) + 1