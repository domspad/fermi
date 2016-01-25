
from traits.api import HasTraits, Instance, Button 
from traitsui.api import View, Item, ModelView, OKCancelButtons, TableEditor, ObjectColumn, Action, Handler, Menu

from fermi.model.database import Database

class Database_Handler(Handler):

	def do_edit_selected(self,info):
		print "fired?"
		import ipdb; ipdb.set_trace()


do_edit_selected = Action(name = "Edit",
						action = "do_edit_selected")



class DatabaseView(HasTraits):

	model = Instance(Database)

	edit_button = Button(label='EditButton')

	def default_traits_view(self):
		
		estimates_table_ed = TableEditor(
			columns=[
				ObjectColumn(name='name'),
			],
			# menu = Menu(handler.do_edit_selected),
			auto_size=True,
			editable=False 	#Can still select rows BUT not add them
			# row_factory=True #allows you to "Add new item"
		)

		view = View(
			Item('object.model.estimates',editor=estimates_table_ed),
			Item('object.edit_button'),
			resizable=True, buttons=[do_edit_selected,'Plot','Add','Delete'],
			handler=Database_Handler
		)

		return view

	def _edit_button_fired(self, event):
		import ipdb; ipdb.set_trace()

if __name__ == '__main__':

	db = Database()

	view = DatabaseView(model=db)

	view.configure_traits()
