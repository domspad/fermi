"""
A dialog that will allow the user to specify a new estimate
"""

from traits.api import HasTraits, Str, List, Button, on_trait_change
from traitsui.api import OKCancelButtons, View, Group,VGroup, Item, TableEditor, ObjectColumn

from fermi.model.estimate_proxy import EstimateProxy
from fermi.model.variable_proxy import VariableProxy
from fermi.utils.str_utils import get_var_names


variable_table_editor = TableEditor(
	columns = [
		ObjectColumn(name='name'),
		ObjectColumn(name='low'),
		ObjectColumn(name='high'),
		ObjectColumn(name='notes'),
	],
	deletable=True,
	sort_model=True,
	auto_size=False,
	# edit_view=View(
	# 	Group('name','high','low',show_border=True),
	# 	resizable=True
	# ),
	row_factory=VariableProxy
)

class AddEstimateDialog(HasTraits):

	name = Str

	expressions = List(Str)

	variables = List(VariableProxy)

	estimate_notes = Str

	valid_button = Button(label='Validate')

	def default_traits_view(self):

		view = View(
			VGroup(
				Item('name'),
				Item('expressions', style='text'),
				Item('variables',
					 show_label=False,
					 editor=variable_table_editor),
				Item('estimate_notes', style='text'),
				Item('valid_button',
					 show_label=False),
			),
			buttons=OKCancelButtons,
			resizable=True
		)

		return view

	def create_estimate(self):
		estimate = EstimateProxy()
		estimate.name = self.name
		estimate.expressions = self.expressions
		estimate.variables = self.variables
		estimate.notes = self.estimate_notes
		return estimate

	def _valid_button_fired(self, event):
		# check valid name
		# check valid expression
		# check all variables defined
		print "checking estimate!"
		self._update_variables_names()

	@on_trait_change('expressions')
	def _update_variables_names(self):
		"""
		Add Variable Proxy instance to variables for every new variable name
		found in expressions
		"""
		print 'updating variable names!'
		variable_names = list()
		current_variable_names = [var.name for var in self.variables]

		for expr in self.expressions:
			expr_names = get_var_names(expr)
			for name in expr_names:
				if name in variable_names or name in current_variable_names:
					continue
				else:
					new_var = VariableProxy(name=name)
					self.variables.append(new_var)


if __name__ == '__main__':

	ad = AddEstimateDialog()

	res = ad.configure_traits()

	import ipdb; ipdb.set_trace()