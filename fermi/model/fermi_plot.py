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
from chaco.tools.api import PanTool, ZoomTool, RangeSelection, RangeSelectionOverlay

COLORS = ['red', 'blue', 'green', 'orange']


class FermiPlot(HasTraits):

	plot = Instance(Component)

	data = ArrayPlotData

	n_bins = Int(100)

	n_sims = Int(10000)

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
		"Determines minimum and maximum bin exponent from sample data"
		all_samples = np.concatenate(self._samples.values())
		s_min, s_max = min(all_samples), max(all_samples)
		return int(np.log10(s_min)), int(np.log10(s_max)) + 1

	def _data_default(self):
		data = ArrayPlotData()
		
		# set bins
		min_bin, max_bin = self._get_minmax()
		x = 10 ** np.linspace(min_bin, max_bin, self.n_bins)
		data.set_data("bins", x[:-1])

		# set freqs
		for sample_name in self._samples:
			samples = self._samples[sample_name]
			freqs, bin_edges = np.histogram(samples, bins=x)
			probs = freqs / float(self.n_sims)
			data.set_data(sample_name, probs)

		return data

	def _plot_default(self):
		self.data = self._data_default()

		plot = Plot(self.data)

		for ii, s_name in enumerate(self._samples):
			color = COLORS[ii % len(self._samples)]
			plot.plot(('bins',s_name), name=s_name,
					   type='filled_line',
					   edge_color=color,
					   face_color=color,
					   alpha=0.5,
					   bgcolor='white',
					   render_style='hold') # render_style determines whether interpolate

		plot.index = plot._get_or_create_datasource('bins') #set index name manually so range selection works
		plot.index_scale = 'log'
		plot.title = 'Fermi Plot'
		plot.padding = 50
		plot.legend.visible = True

		plot.tools.append(PanTool(plot))
		plot.active_tool = RangeSelection(plot)
		plot.overlays.append(RangeSelectionOverlay(component=plot))
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
