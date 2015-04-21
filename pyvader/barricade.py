import pygame

class Barricade(object):
    def __init__(self):
        # List of sections with lives
        lives_for_section = 4
        num_sections = 10
        self.barricade_info = []
        for i in range(0, num_sections):
            self.barricade_info.append(lives_for_section)
            
    def num_sections(self):
        return len(self.barricade_info)

    def lives_for_section(self, index_of_section):
        return self.barricade_info[index_of_section]

    def damage_section(self, index_of_section):
        self.barricade_info[index_of_section] -= 1
