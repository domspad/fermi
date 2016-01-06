
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import log10, floor

def round_sig(x, sig=2):
	return round(x, sig-int(floor(log10(x)))-1)

class Estimate:
	"""
	name
	units
	component_dict
	expression
	num_runs
	source
	actual
	"""

	def __init__(self, name='', var_name='a', component_dict=None, expression_str='2',actual=100, source='www.blah.com', **kwargs):
		self.name = name
		self.var_name = var_name
		self.expression_str = expression_str
		self.actual = actual
		self.source = source
		self.component_dict = component_dict

	def sample(self):
		namespace = {name: comp.sample() for (name,comp) in self.component_dict.items()}
		return eval(self.expression_str, namespace)

	def simulate(self, num_runs):
		"""
		sets self.data to be list of results from 'num_runs' worth of simulations
		"""
		self.data = pd.Series([self.sample() for ii in xrange(num_runs)])

	def get_posterior(self):
		"""
		returns f:Real --> [0,1] function based on data (kernel density?)
		"""
		# set data if not already there
		if getattr(self,'data') is None:
			self.simulate(self.num_runs)
		# interpolate!
		f = lambda x: np.random.rand()
		return f

	def plot(self):
		"""
		returns a plot of self
		"""
		fig, ax = plt.subplots()
		MIN, MAX = min(self.data), max(self.data)
		res = self.data.hist(ax=ax,bins = 10 ** np.linspace(np.log10(MIN), np.log10(MAX), 50))
		# from ipdb import set_trace;set_trace()
		ax.set_xscale('log')
		median = round_sig(self.data.median())
		ax.set_title(self.name)
		ax.axvline(median)
		ax.axvline(self.actual,color='red')
		plt.annotate('median: {}\nactual: {}'.format(median,self.actual), xy=(0.05, 0.95), xycoords='axes fraction')
		# ylow,yhigh = ax.get_ylim()
		# xlow,xhigh = ax.get_xlim()
		# yan = ylow + (0.85*(yhigh - ylow))
		# xan = xlow + (0.25*(xhigh - xlow))
		# ax.annotate('median: {}'.format(median), xy=(median, yan), xytext=(xan,yan),
		# 			arrowprops=dict(facecolor='black', shrink=0.05))

		fig, ax = plt.subplots()
		self.data.plot(ax=ax,kind='kde',logx=True)
		ax.set_title(self.name)
		ax.axvline(self.data.median())
		ax.axvline(self.actual,color='red')
		plt.annotate('median: {}\nactual: {}'.format(median,self.actual), xy=(0.05, 0.95), xycoords='axes fraction')
		# ylow,yhigh = ax.get_ylim()
		# xlow,xhigh = ax.get_xlim()
		# yan = ylow + (0.85*(yhigh - ylow))
		# xan = xlow + (0.25*(xhigh - xlow))
		# ax.annotate('actual: {}'.format(self.actual), xy=(self.actual, yan), xytext=(xan,yan),
		# 			arrowprops=dict(facecolor='black', shrink=0.05))
		plt.show(block=True)
