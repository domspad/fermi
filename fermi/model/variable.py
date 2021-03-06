
from traits.api import HasTraits, Str, Float, Either
from traitsui.api import View, Item

class Variable(HasTraits):

	name = Str

	low = Float

	high = Float

	mode = Either(None, Float)

	confidence_level = Float(0.90)


if __name__ == '__main__':

	v = Variable()

	v.configure_traits()