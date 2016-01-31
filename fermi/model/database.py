
import json
import pickle

from traits.api import HasTraits, Instance

DATABASE_FILE = '/Users/dominicspadacene/Desktop/fermi/fermi/database.json'
PICKLE_FILE = '/Users/dominicspadacene/Desktop/fermi/fermi/database.p'

from traits.api import Str, Instance, List, Float
from math import sqrt
from scipy.stats import triang
class VariableProxy(HasTraits):
	name = Str
	high = Float
	low = Float

	def sample(self, n=1):
		left, right = self.low, self.high
		mode = sqrt(left * right)
		c = (mode - left) / (right - left)
		loc = left
		scale = right - left
		return triang.rvs(c=c, loc=loc, scale=scale, size=n)


import numpy as np
class EstimateProxy(HasTraits):
	name = Str
	expressions = List(Str)
	variables = List(Instance(VariableProxy))

	def sample(self, n=1, expression_no=0):
		# defaults to sampling first expression

		# get samples
		samples = {var.name: var.sample(n) for var in self.variables}

		# create namespaces
		estimate_samples = []
		for i in xrange(n):
			namespace = {k: samples[k][i] for k in samples}
			estimate_samples.append(eval(self.expressions[expression_no], namespace))

		return np.array(estimate_samples)

class Database(HasTraits):

	name = Str('Fermis')
	estimates = List(Instance(EstimateProxy))
	_file = Str(DATABASE_FILE)
	_pickle_file = Str(PICKLE_FILE)

	def __init__(self):
		pass
		# self.load_json_file()

	# def load_json_file(self):
	# 	estimates = []

	# 	# load json
	# 	with open(DATABASE_FILE, 'r') as f:
	# 		data = json.load(f)

	# 	for estimate_data in data:

	# 		# get vars
	# 		variables = [VariableProxy(**var_data)
	# 					 for var_data in estimate_data['variables']]
	# 		estimate = EstimateProxy()

	# 		# append new estimate
	# 		estimate_load_data = estimate_data
	# 		estimate_load_data['variables'] = variables
	# 		estimates.append(EstimateProxy(**estimate_load_data))

	# 	self.estimates = estimates

	# def save_to_file(self):
	# 	# overwrite data file!
	# 	with open(self._file, 'w') as f:
	# 		json.dump(f)

	def pickle(self):
		with open(self._pickle_file,'w') as f:
			pickle.dump(self,f)


def load_pickle():
	with open(PICKLE_FILE) as f:
		return pickle.load(f)



# Major library imports
import numpy as np
from numpy import exp, linspace, sqrt
from scipy.special import gamma
# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance, Int, Dict, List, Any, Str
from traitsui.api import Item, Group, View, VGroup
# Chaco imports
from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import PanTool, ZoomTool


class FermiPlot(HasTraits):

	plot = Instance(Component)

	data = ArrayPlotData

	n_bins = Int(50)

	n_sims = Int(3000)

	_samples = Dict

	estimates = Any

	def __samples_default(self):
		_samples = {}
		for estimate in self.estimates:
			name_base = estimate.name
			for ii, expr in enumerate(estimate.expressions):
				name = name_base + '.' + str(ii)
				samples = estimate.sample(n=self.n_sims, expression_no=ii)
				_samples[name] = samples
		return _samples

	def _get_minmax(self):
		return 10 ** 0, 10 ** 6

	def _data_default(self):
		data = ArrayPlotData()
		
		# set bins
			# take MIN, MAX of samples as max
		MIN, MAX = self._get_minmax()
		x = 10 ** np.linspace(np.log10(MIN), np.log10(MAX), self.n_bins)
		data.set_data("bins", x[:-1])

		# set freqs
		for sample_name in self._samples:
			samples = self._samples[sample_name]
			freqs, bin_edges = np.histogram(samples, bins=x)
			data.set_data(sample_name, freqs)

		return data

	def _plot_default(self):
		self.data = self._data_default()

		plot = Plot(self.data)

		for s_name in self._samples:
			plot.plot(('bins',s_name), name=s_name)

		plot.index_scale = 'log'
		plot.title = 'Fermi Plot'
		plot.padding = 50
		plot.legend.visible = True

		plot.tools.append(PanTool(plot))
		zoom = ZoomTool(component=plot, tool_mode='box', always_on=False)
		plot.overlays.append(zoom)

		import ipdb; ipdb.set_trace()

		return plot	

	def _default_traits_view(self):
		return View(
			VGroup(
				Item('plot', editor=ComponentEditor(),
					 show_label=False),
				resizable=True
			)
        )

	# @on_trait_change('n_sims')
	# def redraw_plot(self):


if __name__ == '__main__':

	# database = Database()

	# database.pickle()

	db2 = load_pickle()

	# demo = Demo()
	# demo.configure_traits()

	# LOOKING AT SAMPLES
	# est = db2.estimates[0]
	# samples = est.sample()

	fplot = FermiPlot(estimates=[db2.estimates[0]])
	fplot.configure_traits()


