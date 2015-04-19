from nose.tools import *
from pyvader import player

class TestPlayer:
    def setup(self):
        print "Setup"
        self.player = player.Player()

    def teardown(self):
        print "Teardown"
        # Delete stuff?

    def test_player_exists(self):
        assert_not_equal(self.player, None)

    def test_has_lives(self):
        assert_true(self.player.get_lives() > 0)

    def test_lose_life(self):
        initial_lives = self.player.get_lives()
        self.player.take_damage()
        print initial_lives
        print self.player.get_lives()
        assert_true(self.player.get_lives() < initial_lives) 

    def test_fire_player_missile(self):
        # Not entirely sure what the design of this will be
        assert_true(self.player.fire())

#class PlayerTests(unittest.TestCase):
#    def setUp(self):
#        self.player = player.Player()
#    def test_init_player(self):
#        self.assertNotEqual(self.player, None, "Player doesn't exist")
#
#if __name__ == '__main__':
#    unittest.main()
