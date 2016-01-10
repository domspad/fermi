
from traits.api import HasTraits, Str, Dict, Float


class Estimate(HasTraits):

	name = Str

	expr = Str

	# FIXME: Later we will want this to populate itself from expression
	_variables = Dict(Str, Float)





if __name__ == '__main__':
		
	e = Estimate(**{'name': 'num_planes', 'expr': '1 + a', '_variables': {'a': 3.0}})

	e.print_traits()

	print eval(e.expr, e._variables)