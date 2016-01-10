
from math import sqrt

from scipy.stats import triang

class Component:
	"""
	name
	var_name
	low90
	high90
	geomean
	units
	actual
	source

	"""

	def __init__(self, name='a',var='v',low90=0.0,high90=1.0,actual=0.3,source='yomomma',guess=None):
		self.name = name
		self.var = var
		self.low90 = low90
		self.high90 = high90
		self.geomean = sqrt(self.low90 * self.high90)
		self.actual = actual
		self.source = source
		self.guess = guess


	def sample(self):
		left, right, mode = self.low90, self.high90, self.geomean
		c = (mode - left) / (right - left)
		loc = left
		scale = right - left
		return triang.rvs(c=c, loc=loc, scale=scale)

	def show(self):
		"""plots belief"""
		pass