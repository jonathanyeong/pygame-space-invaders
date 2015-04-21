from nose.tools import *
from pyvader import barricade

class TestBarricade:
    def setup(self):
        self.barricade = barricade.Barricade()

    def test_barricade_exists(self):
        assert_not_equal(self.barricade, None)

    def test_number_of_barricade_sections(self):
        # According to the rules
        # There are 10 sections that make up a barricade
        expected_sections = 10
        assert_equal(expected_sections, self.barricade.num_sections(),
                     "Not enough sections")

    def test_number_of_lives_for_a_section(self):
        expected_lives = 4
        index = 0
        assert_equal(expected_lives, self.barricade.lives_for_section(index),
                     "Not enough lives for section")

    def test_damage_section(self):
        index = 0
        initial_life = self.barricade.lives_for_section(index)
        self.barricade.damage_section(index)
        current_life = self.barricade.lives_for_section(index)
        assert_true(initial_life > current_life, "Section should take damage")

