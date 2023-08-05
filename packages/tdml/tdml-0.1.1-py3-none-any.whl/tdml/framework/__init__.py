import os
import sys
import importlib
from . import framework

def get_framework():
	framework_name = "numpy"
	if 'TDML_FRAMEWORK' in os.environ:
		framework_name = os.getenv('TDML_FRAMEWORK')
	if framework_name not in ['pytorch', 'numpy', 'tensorflow']:
		print('Unsupported "{}" as the ML framework, using "numpy" instead.'.format(framework_name))
		framework_name = 'numpy'
	return framework_name

chosen_module = importlib.import_module('.{}'.format(get_framework()), __name__)
curr_module = sys.modules[__name__]

abstract_functions = set(['dtype', 'array', 'astype', \
		'concatenate', 'expand_axis', 'unique', 'tolist', \
		'shape', 'max', 'index_select'])

for abstract_func in abstract_functions:
	material_func = chosen_module.__dict__[abstract_func]
	if abstract_func != 'dtype':
		setattr(curr_module, abstract_func, material_func)
	else:
		dtypes = material_func()
		for dtype in dtypes:
			setattr(curr_module, dtype, dtypes[dtype])
setattr(curr_module, 'framework', get_framework())