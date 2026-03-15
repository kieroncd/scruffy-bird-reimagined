import pygame
from ui.outlinetext import OutlinedText


class ScoreCounter:

    def __init__(self, x=125, y=40):
        self.score = 0
        self.x, self.y = x, y
        self.counter = OutlinedText(f"{self.score}", pygame.font.SysFont("Agency FB", 24), x=self.x, y=self.y)

    def add_score(self, amount=1):
        self.score += amount
        self.counter.set_text(f'{self.score}')
        self.counter.update(0)

    def update(self, delta):
        self.counter.update(delta)

    def render(self, screen):
        self.counter.render(screen)