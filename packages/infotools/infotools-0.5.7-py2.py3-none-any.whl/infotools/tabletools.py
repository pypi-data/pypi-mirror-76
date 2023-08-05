from pathlib import Path
from typing import Union

import pandas


def read_table(file_name: Union[str, Path], **kwargs):
	""" Reads the table and returns a dataframe. This is basically just a short script that lets
		users import data without having to worry about filetype.
	"""
	file_name = Path(file_name)
	extension = file_name.suffix
	default_args = {
		'.csv': {'delimiter': ','},
		'.tsv': {'delimiter': '\t'}
	}

	# arguments = self._cleanArguments(extension, arguments)
	file_name = str(file_name.absolute())
	if extension in {'.xls', '.xlsx', '.xlsm'}:  # .xlsm is not a typo.

		df = pandas.read_excel(file_name, **kwargs)
	elif extension in {'.csv', '.tsv', '.fsv', '.txt'}:
		arguments = {**default_args.get(extension), **kwargs}
		if 'sheetname' in arguments: arguments.pop('sheetname')
		df = pandas.read_table(file_name, **arguments)
	elif extension == '.pkl':
		df = pandas.read_pickle(file_name)
	else:
		raise NameError("{} does not have a valid extension!".format(file_name))
	return df
