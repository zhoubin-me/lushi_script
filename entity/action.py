# -*- coding: utf-8 -*-

class Action:
    def __init__(self, hero, spell, target):
        self.hero = hero
        self.target = target
        self.spell = spell

    def __lt__(self, other):
        return self.spell < other.spell
