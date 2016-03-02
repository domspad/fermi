import re

VAR_NAME_PATTERN = re.compile(ur'[_a-zA-Z]\w+')

def get_var_names(expr):
	"""
	Parse expr for variable names.
	"""
	return VAR_NAME_PATTERN.findall(expr)