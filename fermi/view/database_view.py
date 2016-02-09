
from traits.api import HasTraits, Instance, Button, List
from traitsui.api import View, Item, ModelView, OKCancelButtons, TableEditor, ObjectColumn, Action, Handler, Menu, HGroup

from fermi.model.database import Database, load_pickle
from fermi.model.fermi_plot import FermiPlot
from fermi.view.add_estimate_dialog import AddEstimateDialog

# class Database_Handler(Handler):

# 	def do_edit_selected(self,info):
# 		print "handler-defined button fired"

# 	def save_db(self, info):
# 		import ipdb; ipdb.set_trace()


# do_edit_selected = Action(name = "Edit",
# 						  action = "do_edit_selected")

# do_save_db = Action(name='Save',
# 					action='save_db')

from traits.api import Event
# class EstimateEditor(TableEditor):
	
# 	dclick = Event

# 	def _on_dclick(self, index):
# 		import ipdb; ipdb.set_trace()
# 		print "cell {}".format(index)


class DatabaseView(HasTraits):

	model = Instance(Database)

	edit_button = Button(label='Edit')
	save_button = Button(label='Save')
	add_button = Button(label='Add')
	delete_button = Button(label='Delete')
	plot_button = Button(label='Plot')

	_selected_indices = List

	def default_traits_view(self):
		
		estimates_table_ed = TableEditor(
			columns=[
				ObjectColumn(name='name'),
			],
			# menu = Menu(handler.do_edit_selected),
			auto_size=True,
			selection_mode='rows',
			selected_indices='_selected_indices',
			editable=False, 	#Can still select rows BUT not add them
			# row_factory=True #allows you to "Add new item"
		)

		self.table_ed = estimates_table_ed

		view = View(
			Item('object.model.estimates',editor=estimates_table_ed),
			HGroup(
				Item('object.edit_button',show_label=False),
				Item('object.save_button',show_label=False),
				Item('object.add_button',show_label=False),
				Item('object.delete_button',show_label=False),
				Item('object.plot_button',show_label=False),
			),
			resizable=True, #buttons=[do_edit_selected,'Plot','Add','Delete',do_save_db],
			#handler=Database_Handler
		)

		return view

	def _add_button_fired(self, event):
		print "add dialog opening"
		add_dialog = AddEstimateDialog()
		ok = add_dialog.edit_traits(kind='modal')
		if ok:
			estimate = add_dialog.create_estimate()
			self.model.estimates.append(estimate)
			print "new estimate added!"
		else:
			print "no new estimate created!"
			pass

	def _save_button_fired(self, event):
		self.model.pickle()
		print "Database saved to file"

	def _delete_button_fired(self, event):
		if len(self._selected_indices) != 0:
			rows = set([r for r,c in self._selected_indices])
			for ii in rows:
				estimate = self.model.estimates.pop(ii)
				print "Deleting estimate {}".format(estimate.name)
		else:
			print "Select something to delete"

	def _edit_button_fired(self, event):
		# ensure only one highlighted (or use right-click)
		# create view and populate with this model
		# once return if 'OK' replace the original estimate else discard
		if len(self._selected_indices) == 1:
			row, _  = self._selected_indices[0]
			estimate = self.model.estimates[row]
			print "editing {}".format(estimate.name)
			kws = {}
			kws['name'] = estimate.name
			kws['expressions'] = estimate.expressions[:]
			kws['variables'] = estimate.variables[:]
			add_dialog = AddEstimateDialog(**kws)
			ok = add_dialog.edit_traits(kind='modal')
			if ok:
				new_estimate = add_dialog.create_estimate()
				self.model.estimates[row] = new_estimate
		else:
			print "Select only one row to edit"
		pass

	def _plot_button_fired(self, event):
		if len(self._selected_indices) != 0:
			rows = set([r for r,c in self._selected_indices])
			selected_estimates = [self.model.estimates[ii] for ii in rows]
			fplot = FermiPlot(estimates=selected_estimates)
			fplot.configure_traits()
		else:
			print "please select at least one row"


if __name__ == '__main__':

	db = load_pickle()

	view = DatabaseView(model=db)

	view.configure_traits()
