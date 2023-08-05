import os
import sys
import importlib
from . import dataframe

def get_dataframe():
	dataframe_name = 'pandas'
	if 'TDML_DATAFRAME' in os.environ:
		dataframe_name = os.getenv('TDML_DATAFRAME')
	if dataframe_name not in ['pandas', 'pyspark']:
		print('Unsupported "{}" as the dataframe, using "pandas" instead.'.format(dataframe_name))
		dataframe_name = 'pandas'
	return dataframe_name

chosen_module = importlib.import_module('.{}'.format(get_dataframe()), __name__)
curr_module = sys.modules[__name__]

abstract_functions = set(['toPandas'])

for abstract_func in abstract_functions:
	material_func = chosen_module.__dict__[abstract_func]
	setattr(curr_module, abstract_func, material_func)
setattr(curr_module, 'dataframe', get_dataframe())