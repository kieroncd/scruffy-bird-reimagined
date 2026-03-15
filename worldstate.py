import pygame


class WorldState:

    def __init__(self):
        self.state = {
            "gravity": 10,
            "pipe_speed": 150,
            "pipe_spacing": 300,
            "powerup": False,
            "expires": pygame.time.get_ticks()
        }
        self.temp = None

    def add_modifier(self, modifier):
        self.temp = self.state[modifier.key]
        self.state[modifier.key] = modifier.amount
        self.state["powerup"] = True
        self.state["expires"] = pygame.time.get_ticks() + modifier.duration

    def remove_modifier(self, modifier):
        self.state[modifier.key] = self.temp
        self.state["powerup"] = False

class WorldModifier:

    def __init__(self, key, amount, duration):
        self.key = key
        self.amount = amount
        self.duration = duration