
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
from numpy import exp, linspace, sqrt
from scipy.special import gamma
# Enthought library imports
from enable.api import Component, ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, Group, View
# Chaco imports
from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import PanTool, ZoomTool
import numpy as np

# class FermiPlot(HasTraits):

# 	plot = Plot

# 	data = ArrayPlotData

# 	def _plot_default(self):

# 		MIN, MAX = min(self.data), max(self.data)
# 		x = 10 ** np.linspace(np.log10(MIN), np.log10(MAX), 50)
# 		res = self.data.hist(ax=ax,bins = 10 ** np.linspace(np.log10(MIN), np.log10(MAX), 50))



# def _create_plot_comp():

# 	plot.index_scale = 'log'

def _create_plot_component():

	# Create some x-y data series to plot
	x = linspace(1.0, 8.0, 200)
	pd = ArrayPlotData(index = x)
	pd.set_data("y0", sqrt(x))
	pd.set_data("y1", x)
	pd.set_data("y2", x**2)
	pd.set_data("y3", exp(x))
	pd.set_data("y4", gamma(x))
	pd.set_data("y5", x**x)

	# Create some line plots of some of the data
	plot = Plot(pd)
	plot.plot(("index", "y0"), line_width=2, name="sqrt(x)", color="purple")
	plot.plot(("index", "y1"), line_width=2, name="x", color="blue")
	plot.plot(("index", "y2"), line_width=2, name="x**2", color="green")
	plot.plot(("index", "y3"), line_width=2, name="exp(x)", color="gold")
	plot.plot(("index", "y4"), line_width=2, name="gamma(x)",color="orange")
	plot.plot(("index", "y5"), line_width=2, name="x**x", color="red")

	# Set the value axis to display on a log scale
	plot.value_scale = "log"

	# Tweak some of the plot properties
	plot.title = "Log Plot"
	plot.padding = 50
	plot.legend.visible = True

	# Attach some tools to the plot
	plot.tools.append(PanTool(plot))
	zoom = ZoomTool(component=plot, tool_mode="box", always_on=False)
	plot.overlays.append(zoom)

	return plot

# Attributes to use for the plot view.
size=(900,500)
title="Basic x-y log plots"

class Demo(HasTraits):
	plot = Instance(Component)

	traits_view = View(
					Group(
						Item('plot', editor=ComponentEditor(size=size),
							 show_label=False),
						orientation = "vertical"),
					resizable=True, title=title
					)

	def _plot_default(self):
		return _create_plot_component()



if __name__ == '__main__':

	# database = Database()

	# database.pickle()

	db2 = load_pickle()

	# demo = Demo()
	# demo.configure_traits()



