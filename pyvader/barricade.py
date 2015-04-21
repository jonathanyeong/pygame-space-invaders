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
        if (self.barricade_info[index_of_section] > 0):
            self.barricade_info[index_of_section] -= 1

    def is_section_destroyed(self, index_of_section):
        if (self.barricade_info[index_of_section] == 0):
            return True
        return False

    def is_destroyed(self):
        num_sections_destroyed = 0
        for i in self.barricade_info:
            if (i == 0):
                num_sections_destroyed += 1
        if (num_sections_destroyed == self.num_sections()):
            return True
        return False
