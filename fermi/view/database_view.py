
from traits.api import HasTraits, Instance, Button 
from traitsui.api import View, Item, ModelView, OKCancelButtons, TableEditor, ObjectColumn, Action, Handler, Menu, HGroup

from fermi.model.database import Database, load_pickle, EstimateProxy, VariableProxy

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

	def default_traits_view(self):
		
		estimates_table_ed = TableEditor(
			columns=[
				ObjectColumn(name='name'),
			],
			# menu = Menu(handler.do_edit_selected),
			auto_size=True,
			editable=False, 	#Can still select rows BUT not add them
			# row_factory=True #allows you to "Add new item"
		)

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

	def _save_button_fired(self, event):
		# self.model.pickle()
		print "Database saved to file"

	def _delete_button_fired(self, event):
		print "Deleting selected item"

	def _edit_button_fired(self, event):
		print "view-defined button fired"

if __name__ == '__main__':

	db = load_pickle()

	view = DatabaseView(model=db)

	view.configure_traits()
