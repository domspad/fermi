"""
A dialog that will allow the user to specify a new estimate
"""

from traits.api import HasTraits, Str, List, Button
from traitsui.api import OKCancelButtons, View, Group,VGroup, Item, TableEditor, ObjectColumn

from fermi.model.estimate_proxy import EstimateProxy
from fermi.model.variable_proxy import VariableProxy


variable_table_editor = TableEditor(
	columns = [
		ObjectColumn(name='name'),
		ObjectColumn(name='high'),
		ObjectColumn(name='low'),
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

	valid_button = Button(label='Validate')

	def default_traits_view(self):

		view = View(
			VGroup(
				Item('name'),
				Item('expressions'),
				Item('variables',
					 show_label=False,
					 editor=variable_table_editor),
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
		return estimate

	def _valid_button_fired(self, event):
		# check valid name
		# check valid expression
		# check all variables defined
		print "checking estimate!"


if __name__ == '__main__':

	ad = AddEstimateDialog()

	res = ad.configure_traits()

	import ipdb; ipdb.set_trace()