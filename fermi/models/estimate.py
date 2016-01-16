
import re

from traits.api import HasTraits, Str, Dict, Float, Property, List

VAR_NAME_PATTERN = re.compile(ur'\$[\w_]+')

class Estimate(HasTraits):

	name = Str

	#: vars marked with '$' and will parse
	expr = Str

	#: '$' removed from expr
	_clean_expr = Property(depends_on='expr')

	# FIXME: Later we will want this to populate itself from expression
	_variable_list = Property(List(Str),depends_on='expr')

	# _variable_dict = Property(Dict(Str,Float),depends_on='_variable_list')

	def _get__clean_expr(self):
		return self.expr.replace('$','')

	def _get__variable_list(self):
		var_set = set([m.group(0).replace('$','') for m in VAR_NAME_PATTERN.finditer(self.expr)])
		return list(var_set)

	# def _get__variable_dict(self):



from traits.api import Instance
from traitsui.api import View, VGroup, Item

class EstimateView(HasTraits):

	model = Instance(Estimate)

	def default_traits_view(self):

		return View(
			VGroup(
				Item('object.model.name'),
				Item('object.model.expr'),
			)
		)


if __name__ == '__main__':
		
	e = Estimate(**{'name': 'num_planes', 'expr': '1 + $a ** $another'})

	e_view = EstimateView(model=e)


	e_view.configure_traits()

	print e._clean_expr, e._variable_list
	# print eval(e._clean_expr, e._variables)