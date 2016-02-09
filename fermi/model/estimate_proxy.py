import numpy as np

from traits.api import Str, HasTraits, List, Instance

from fermi.model.variable_proxy import VariableProxy


class EstimateProxy(HasTraits):
	name = Str
	expressions = List(Str)
	variables = List(Instance(VariableProxy))

	# random notes user can make about estimate
	notes = Str

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