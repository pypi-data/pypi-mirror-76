import re
import types
import numpy as np
from . import framework as arr
from . import dataframe as dframe
from .data import *

class Dataset():
	"""
	The dataset class of TDML.

	Args:
		df: The dataframe such as :class:`pandas.Dataframe`.
		**kwargs: Argument list include `label`, `feature` and `text`.
	"""

	def __init__(self, df, **kwargs):
		self.df = dframe.toPandas(df)
		self.user_keys = kwargs
		self.label_mapping = None
		self.feature_mapping = None
		self.columns = self.df.columns.values
		self._validate_key()

	@property
	def num_sample(self) -> int:
		"""
		The number of samples in the dataset.
		"""
		return arr.shape(self.feature)[0]

	@property
	def num_feature(self) -> int:
		"""
		The dimension of the data features.
		"""
		return arr.shape(self.feature)[1]

	@property
	def num_label(self) -> int:
		"""
		The number of labels if the label column is specified.
		"""
		if self.label_key is None:
			return 0
		return arr.max(self.label, axis=0) + 1

	def __getattr__(self, attr):
		if attr in ['train_x', 'train_y', 'test_x', 'test_y', 'val_x', 'val_y']:
			attr_private = '_' + attr
			if attr_private not in self.__dict__:
				return None
			return self.__dict__[attr_private].data
		return self.get(attr)

	def idx_to_feature(self, idx) -> str:
		"""
		Return feature name by given the index or indices in the feature array.

		Args:
			idx (int or tuple): The index or indices of the feature array.

		Returns:
			The string feature name at the position of specified ndex or indices in the feature array.
		"""
		if type(idx) != tuple and (idx < 0 or idx >= len(self._feature_keys)):
			raise ValueError('The index is out of range.')
		return self._idx_feature[idx]

	def feature_to_idx(self, feature) -> int or tuple:
		"""
		Return index of the given feature name in the feature array.

		Args:
			feature (str): The string of the feature name.

		Returns:
			(int or tuple): The index of the given feature name in the feature array.
		"""
		if feature not in self._feature_keys:
			raise ValueError('Feature is not in the feature list.')
		return self._feature_idx[feature]

	def transform(self, **kwargs):
		"""
		Transform the dataframe into the arrays for specified `label`, `feature` and `text`.
		User can also specify text transform function to transform the selected `text` feature.
		"""
		self._update_label()
		self._update_feature(**kwargs)
		
	def _update_label(self):
		if self.label_key is None:
			self.label = None
			return
		raw_labels = self.df[self.label_key].values
		label_type = type(raw_labels[0])
		if label_type == str:
			self.label, self.label_mapping = self._one_hot_from_str(raw_labels)
		elif label_type == int or label_type == np.bool_:
			self.label = arr.array(raw_labels, dtype=arr.int64)
		else:
			self.label = arr.array(raw_labels, dtype=arr.float32)
		self._validate_label()

	def _update_feature(self, **kwargs):
		if self.label_key is None and self.feature_key is None:
			feature_keys = [key for key in self.df.columns.values]
		elif self.feature_key is None:
			feature_keys = [key for key in self.df.columns.values if key != self.label_key]
		else:
			if isinstance(self.feature_key, str):
				feature_keys = [self.feature_key]
			else:
				feature_keys = self.feature_key

		self._idx_feature = {}
		self._feature_idx = {}
		self._feature_keys = feature_keys
		features_list = []
		mappings = {}
		for i, feature_key in enumerate(self._feature_keys):
			raw_feature = self.df[feature_key].values
			feature_type = type(raw_feature[0])
			if feature_type == str and self.text_key != feature_key:
				curr_feature, feature_mapping = self._one_hot_from_str(raw_feature)
				curr_feature = arr.astype(curr_feature, arr.float32)
				mappings[feature_key] = feature_mapping
			elif self.text_key == feature_key:
				if 'text_transform' in kwargs:
					func = kwargs['text_transform']
					kwargs_new = kwargs.copy()
					kwargs_new.pop('text_transform')
					curr_feature, feature_mapping = func(sentences=raw_feature, **kwargs_new)
					curr_feature = arr.array(curr_feature)
				else:
					func = self._bag_of_word
					curr_feature, feature_mapping = func(sentences=raw_feature)
				curr_feature = arr.astype(curr_feature, arr.float32)
				mappings[feature_key] = feature_mapping
			else:
				curr_feature = arr.array(raw_feature, dtype=arr.float32)

			if self.text_key == feature_key:
				features_list.append(curr_feature)
				idx_s = i
				idx_e = i + len(curr_feature[0])
				self._idx_feature[(idx_s, idx_e)] = feature_key
				self._feature_idx[feature_key] = (idx_s, idx_e)
			else:
				features_list.append(arr.expand_axis(curr_feature, axis=1))
				self._idx_feature[i] = feature_key
				self._feature_idx[feature_key] = i

		if mappings != {}:
			self.feature_mapping = mappings
		self.feature = arr.concatenate(features_list, axis=1)

	def _bag_of_word(self, sentences):
		words = set()
		processed_sentences = []
		for sentence in sentences:
			s = re.sub(r'[^\w\s]', '', sentence).lower()
			s = s.split(' ')
			processed_sentence = []
			for item in s:
				if item != '':
					words.add(item)
					processed_sentence.append(item)
			processed_sentences.append(processed_sentence)
		words = sorted(list(words))
		mapping = {}
		for item in zip(words, range(len(words))):
			word = item[0]
			idx = item[1]
			mapping[word] = idx
		feature = []
		num = len(mapping)
		for processed_sentence in processed_sentences:
			temp_feature = [0] * num
			for word in processed_sentence:
				idx = mapping[word]
				temp_feature[idx] = 1
			feature.append(temp_feature)
		return arr.array(feature), mapping

	def _validate_key(self):
		self.label_key = None
		self.feature_key = None
		self.text_key = None

		# Assign user_keys to keys
		for key in self.user_keys:
			if key == 'label':
				self.label_key = self.user_keys[key]
			elif key == 'feature':
				self.feature_key = self.user_keys[key]
			elif key == 'text':
				self.text_key = self.user_keys[key]

		# Validate the keys
		if self.label_key is not None and not isinstance(self.label_key, str):
			raise ValueError('Instead of {}, the label key should be string \
				type.'.format(type(self.label_key)))
		if self.feature_key is not None:
			feature_type = type(self.feature_key)
			if feature_type != str and feature_type != list:
				raise ValueError('Instead of {}, the feature key should be string or \
					list type.'.format(type(self.feature_key)))

		if self.label_key is not None and self.feature_key is not None and self.label_key in self.feature_key:
			raise ValueError('The label key {} should not be in the feature \
				key.'.format(self.label_key))

		if self.text_key is not None and not isinstance(self.text_key, str):
			raise ValueError('Instead of {}, the text key should be string \
				type.'.format(type(self.text_key)))

		if self.text_key is not None:
			if self.label_key is not None and self.text_key == self.label_key:
				raise ValueError('The text key should not overlap with the label key.')
			if self.feature_key is not None and isinstance(self.feature_key, str) \
					and self.text_key == self.feature_key:
				raise ValueError('The text key should not overlap with the feature key.')
			if self.feature_key is not None and isinstance(self.feature_key, list) \
					and self.text_key in self.feature_key:
				raise ValueError('The text key should not overlap with the feature key.')

	def _validate_label(self):
		if 'label_mapping' in self.__dict__:
			if self.label_mapping == None:
				return
			unique_values = arr.tolist(arr.unique(self.label))
			range_values = list(range(min(unique_values), max(unique_values) + 1))
			if all([u_val == r_val for u_val, r_val in zip(unique_values, range_values)]) == False:
				raise ValueError('Label should range from 0 to {}.'.format(max(range_values)))

	def _one_hot_from_str(self, array, mapping=None):
		strings = set()
		for item in array:
			strings.add(item)
		strings = sorted(list(strings))
		mapping = dict(zip(strings, range(len(strings))))
		items = []
		for item in array:
			items.append(mapping[item])
		return arr.array(items, dtype=arr.int64), mapping

	def train_test_split(self, train_size=0.8, test_size=0.2, shuffle=True, seed=None, train_split=None, test_split=None):
		"""
		Split the dataset into train and test set. Sum of `train_size` and `test_size` should be 1.

		Args:
			train_size (float): The ratio of train set. The default value is 0.8.
			test_size (float): The ratio of test set. The default value is 0.2.
			shuffle (bool): Whether the dataset is shuffled before the split. The default value is `True`.
			seed (int): Set the seed for :class:`numpy.random.seed`. The default value is `None`.
			train_split (:class:`numpy.ndarray`): The pre-specified indices of train set in :class:`numpy.ndarray`. The default value is `None`.
			test_split (:class:`numpy.ndarray`): The pre-specified indices of test set in :class:`numpy.ndarray`. The default value is `None`.
		"""
		if train_split is None and test_split is None:
			self._validate_split([train_size, test_size])
			self._reset_split_keys()
			indices = np.arange(self.num_sample, dtype=int)
			train_indices, test_indices = self._indices_split(indices, \
					train_size, shuffle, seed)
		elif train_split is not None and test_split is not None:
			train_indices = np.array(train_split, dtype=int)
			test_indices = np.array(test_split, dtype=int)
		else:
			raise ValueError("Both of the train and test indices should be specified if choosing \
								the prespecified indices.")
		self._train_x = Feature(arr.index_select(self.feature, train_indices))
		self._test_x = Feature(arr.index_select(self.feature, test_indices))
		if self.label_key is not None:
			self._train_y = Label(arr.index_select(self.label, train_indices))
			self._test_y = Label(arr.index_select(self.label, test_indices))

	def train_val_test_split(self, train_size=0.8, val_size=0.1, test_size=0.1, shuffle=True, seed=None, \
							train_split=None, val_split=None, test_split=None):
		"""
		Split the dataset into train, validation and test set. Sum of `train_size`, `val_size` and `test_size` should be 1.

		Args:
			train_size (float): The ratio of train set. The default value is 0.8.
			val_size (float): The ratio of validation set. The default value is 0.1.
			test_size (float): The ratio of test set. The default value is 0.1.
			shuffle (bool): Whether the dataset is shuffled before the split. The default value is `True`.
			seed (int): Set the seed for :class:`numpy.random.seed`. The default value is `None`.
			train_split (:class:`numpy.ndarray`): The pre-specified indices of train set in :class:`numpy.ndarray`. The default value is `None`.
			val_split (:class:`numpy.ndarray`): The pre-specified indices of validation set in :class:`numpy.ndarray`. The default value is `None`.
			test_split (:class:`numpy.ndarray`): The pre-specified indices of test set in :class:`numpy.ndarray`. The default value is `None`.
		"""
		prespecified_indices = [train_split, val_split, test_split]
		if all(item is None for item in prespecified_indices):
			self._validate_split([train_size, val_size, test_size])
			self._reset_split_keys()
			indices = np.arange(self.num_sample, dtype=int)

			train_indices, val_test_indices = self._indices_split(indices, \
					train_size, shuffle, seed)
			val_size_ratio = val_size / (val_size + test_size)
			val_indices, test_indices = self._indices_split(val_test_indices, \
					val_size_ratio, shuffle, seed)
		elif all(item is not None for item in prespecified_indices):
			train_indices = np.array(train_split, dtype=int)
			val_indices = np.array(val_split, dtype=int)
			test_indices = np.array(test_split, dtype=int)
		else:
			raise ValueError("All of the train, validation and test indices should be specified if \
								choosing the prespecified indices.")
		self._train_x = Feature(arr.index_select(self.feature, train_indices))
		self._val_x = Feature(arr.index_select(self.feature, val_indices))
		self._test_x = Feature(arr.index_select(self.feature, test_indices))
		if self.label_key is not None:
			self._train_y = Label(arr.index_select(self.label, train_indices))
			self._val_y = Label(arr.index_select(self.label, val_indices))
			self._test_y = Label(arr.index_select(self.label, test_indices))

	def reshuffle(self, seed=0):
		"""
		Randomly reshuffle the train data for both the feature and label.

		Args:
			seed (int): Set the seed for :class:`numpy.random.seed`. The default value is `0`.
		"""
		np.random.seed(seed)
		if '_reshuffle_indices' not in self.__dict__:
			self._reshuffle_indices = np.arange(self._train_x.num_sample)
		np.random.shuffle(self._reshuffle_indices)
		if '_train_x' in self.__dict__ and '_train_y' in self.__dict__:
			self.__dict__['_train_x'].reshuffle(self._reshuffle_indices)
			self.__dict__['_train_y'].reshuffle(self._reshuffle_indices)

	def _reset_split_keys(self):
		for key in ['_train_x', '_val_x', '_test_x',\
					'_train_y', '_val_y', '_test_y',\
					'reshuffle', 'reshuffle_indices']:
			if key in self.__dict__:
				del self.__dict__[key]
			self.__dict__.pop(key, None)

	def _indices_split(self, indices, size, shuffle, seed):
		if type(seed) == int:
			np.random.seed(seed)
		else:
			np.random.seed(0)
		if shuffle == True:
			np.random.shuffle(indices)
		num = int(len(indices) * size)
		return indices[:num], indices[num:]

	def _validate_split(self, ratios):
		for ratio in ratios:
			if type(ratio) != int and type(ratio) != float:
				raise ValueError('The split ratio should be float.')
		if not np.isclose(np.sum(ratios), 1):
			raise ValueError('The split ratios should sum to 1.')

	def __str__(self):
		string = 'Dataset('
		str_list = []
		keys = ['label', 'feature', '_train_x', '_train_y', \
				'_test_x', '_test_y', '_val_x', '_val_y', \
				'label_mapping', 'feature_mapping']
		special_keys = ['_train_x', '_train_y', '_test_x', \
						'_test_y', '_val_x', '_val_y']
		for i, key in enumerate(keys):
			if key not in self.__dict__:
				val = None
			elif key in ['label', 'feature']:
				if key in self.__dict__ and self.__dict__[key] is not None:
					val = list(arr.shape(self.__dict__[key]))
				else:
					val = None
			elif key in special_keys:
				if self.__dict__[key] is not None:
					val = str(list(arr.shape(self.__dict__[key].data)))
				key = key[1:len(key)]
			elif key in ['label_mapping', 'feature_mapping']:
				if self.__dict__[key] is not None:
					val = len(self.__dict__[key])
				else:
					val = None
			else:
				val = self.__dict__[key]
			if val is None:
				continue
			str_list.append('{}={}'.format(key, val))
		string += ', '.join(str_list)
		string += ')'
		return string
