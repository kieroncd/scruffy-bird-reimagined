import pygame
import numpy as np


class Pipe:

    def __init__(self, sprite, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(f'graphics/{sprite}.png').convert_alpha()
        self.rect = self.sprite.get_rect()

    def update(self, delta, speed=100):
        self.x -= speed * delta
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))

    def render(self, screen):
        screen.blit(self.sprite, self.rect)


class PipePair:

    def __init__(self, x):
        self.x = x
        self.award_points = True
        offset = np.random.randint(-100, 100)
        self.upper = Pipe("pipe_ketchup", self.x, -100 + offset)
        self.lower = Pipe("pipe_mayo", self.x, 200 + offset)

    def update(self, delta, world_state):
        self.check_oob()
        self.upper.update(delta, world_state.state['pipe_speed'])
        self.lower.update(delta, world_state.state['pipe_speed'])
        self.x = self.upper.x

    def render(self, screen):
        self.upper.render(screen)
        self.lower.render(screen)

    def check_oob(self):
        # Checks if pipe is off-screen
        if self.x < -50:
            return True

    def reposition(self, x):
        offset = np.random.randint(-100, 100)
        self.upper.x = x
        self.upper.y = -100 + offset
        self.lower.x = x
        self.lower.y = 200 + offset
        self.x = x
        self.award_points = True
