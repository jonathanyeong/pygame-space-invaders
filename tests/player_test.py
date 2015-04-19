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
    


#class PlayerTests(unittest.TestCase):
#    def setUp(self):
#        self.player = player.Player()
#    def test_init_player(self):
#        self.assertNotEqual(self.player, None, "Player doesn't exist")
#
#if __name__ == '__main__':
#    unittest.main()
