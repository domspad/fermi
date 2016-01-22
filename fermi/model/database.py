
import json
import pickle

from traits.api import HasTraits, Instance

DATABASE_FILE = '/Users/dominicspadacene/Desktop/fermi/fermi/database.json'
PICKLE_FILE = '/Users/dominicspadacene/Desktop/fermi/fermi/database.p'

from traits.api import Str, Instance, List, Float
class VariableProxy(HasTraits):
	name = Str
	high = Float
	low = Float

class EstimateProxy(HasTraits):
	name = Str
	expressions = List(Str)
	variables = List(Instance(VariableProxy))


class Database(HasTraits):

	estimates = List(Instance(EstimateProxy))

	def __init__(self):
		self.load_json_file()

	def load_json_file(self):
		estimates = []

		# load json
		with open(DATABASE_FILE, 'r') as f:
			data = json.load(f)

		for estimate_data in data:

			# get vars
			variables = [VariableProxy(**var_data)
						 for var_data in estimate_data['variables']]
			estimate = EstimateProxy()

			# append new estimate
			estimate_load_data = estimate_data
			estimate_load_data['variables'] = variables
			estimates.append(EstimateProxy(**estimate_load_data))

		self.estimates = estimates

	def save_to_file(self):
		# overwrite data file!
		with open(DATABASE_FILE, 'w') as f:
			json.dump(f)

	def pickle(self):
		with open(PICKLE_FILE,'w') as f:
			pickle.dump(self,f)


def load_pickle():
	with open(PICKLE_FILE) as f:
		return pickle.load(f)

if __name__ == '__main__':

	database = Database()

	database.pickle()

	db2 = load_pickle()




