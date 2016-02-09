
import pickle

from traits.api import HasTraits, Instance, Str, List

from fermi.model.estimate_proxy import EstimateProxy
from fermi.model.variable_proxy import VariableProxy
from fermi.utils.io_util import io_pickle_file




class Database(HasTraits):

	name = Str('Fermis')
	estimates = List(Instance(EstimateProxy))
	_pickle_file = Str

	def __init__(self):
		self._pickle_file = io_pickle_file()
		pass

	def pickle(self):
		with open(self._pickle_file,'w') as f:
			pickle.dump(self,f)


def load_pickle():
	pickle_file = io_pickle_file()
	with open(pickle_file) as f:
		return pickle.load(f)


if __name__ == '__main__':

	# database = Database()

	# database.pickle()

	db2 = load_pickle()

