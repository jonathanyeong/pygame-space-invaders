from nose.tools import *
from pyvader import barricade

class TestBarricade:
    def setup(self):
        self.barricade = barricade.Barricade()

    def test_barricade_exists(self):
        assert_not_equal(self.barricade, None)
