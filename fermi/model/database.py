
import json
import pickle

from traits.api import HasTraits, Instance, Str, List

from fermi.model.estimate_proxy import EstimateProxy
from fermi.model.variable_proxy import VariableProxy

DATABASE_FILE = '/Users/dominicspadacene/Desktop/fermi/fermi/database.json'
PICKLE_FILE = '/Users/dominicspadacene/Desktop/fermi/fermi/database.p'


class Database(HasTraits):

	name = Str('Fermis')
	estimates = List(Instance(EstimateProxy))
	_file = Str(DATABASE_FILE)
	_pickle_file = Str(PICKLE_FILE)

	def __init__(self):
		pass

	def pickle(self):
		with open(self._pickle_file,'w') as f:
			pickle.dump(self,f)


def load_pickle():
	with open(PICKLE_FILE) as f:
		return pickle.load(f)


if __name__ == '__main__':

	# database = Database()

	# database.pickle()

	db2 = load_pickle()

