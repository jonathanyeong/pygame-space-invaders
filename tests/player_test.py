from nose.tools import *
from pyvader import player

class TestPlayer:
    def setup(self):
        self.width = 100
        self.height = 100
        print "Setup"
        boundary = (self.width, self.height)
        self.player = player.Player(boundary)

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

    # Testing that firing works will have to be done via real life
    # def test_fire_player_missile(self):
        # Not entirely sure what the design of this will be
        # assert_true(self.player.fire())


    def test_current_pos_of_player(self):
        assert_not_equal(self.player.position(), None)
    
    def test_move_player_right(self):
        (prevX,y) = self.player.position()
        (x,y) = self.player.move_right()
        print "prevx, ", prevX
        print "x, ", x
        assert_true(x > prevX)

    def test_move_player_left(self):
        (prevX,y) = self.player.position()
        (x,y) = self.player.move_left()
        assert_true(x < prevX)

    def test_player_right_boundary(self):
        boundary = self.width
        for i in range(0, self.width):
            (x,y) = self.player.move_right()
    
        print "x pos: ", x
        assert(x <= boundary)

    def test_player_left_boundary(self):
        boundary = 0
        print "player pos: ", self.player.position()
        for i in range(0, self.width):
            (x,y) = self.player.move_left()
    
        print "x pos: ", x
        assert(x >= -self.player.get_speed())

