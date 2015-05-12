from nose.tools import *
from pyvader import alien


class TestAlien:
    def setup(self):
        self.alien = alien.Alien()

    def test_alien_has_a_type(self):
        assert_not_equal(self.alien.type, None)

    def test_alien_has_correct_type(self):
        check_type = False
        if (self.alien.type == "
        
