from nose.tools import *
from pyvader import player

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

def test_basic():
    print "I RAN!"


#class PlayerTests(unittest.TestCase):
#    def setUp(self):
#        self.player = player.Player()
#    def test_init_player(self):
#        self.assertNotEqual(self.player, None, "Player doesn't exist")
#
#if __name__ == '__main__':
#    unittest.main()
