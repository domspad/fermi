
from fermi.model.database import load_pickle
from fermi.model.fermi_plot import FermiPlot
from fermi.view.database_view import DatabaseView


if __name__ == '__main__':

	db = load_pickle()

	view = DatabaseView(model=db)

	view.configure_traits()

	fplot = FermiPlot(estimates=[db.estimates[0]])

	fplot.configure_traits()