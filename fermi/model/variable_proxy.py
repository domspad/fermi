from traits.api import Str, HasTraits, Float
from math import sqrt
from scipy.stats import triang


class VariableProxy(HasTraits):
	name = Str
	high = Float
	low = Float
	notes = Str

	def sample(self, n=1):
		left, right = self.low, self.high
		mode = sqrt(left * right)
		c = (mode - left) / (right - left)
		loc = left
		scale = right - left
		return triang.rvs(c=c, loc=loc, scale=scale, size=n)


