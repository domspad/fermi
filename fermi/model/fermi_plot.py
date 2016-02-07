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

	#: n_sims number of samples for each expression in each estimate
	#: { name_estimate.expr_no : array[n_sims] }
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

		return plot	

	def default_traits_view(self):
		return View(
			VGroup(
				Item('plot', editor=ComponentEditor(),
					 show_label=False),
			),
			resizable=True
        )
