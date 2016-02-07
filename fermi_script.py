
from fermi.model.database import load_pickle
from fermi.model.fermi_plot import FermiPlot


if __name__ == '__main__':

	db2 = load_pickle()

	fplot = FermiPlot(estimates=[db2.estimates[0]])

	fplot.configure_traits()