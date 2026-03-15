import pygame


class CoolDownTimer:

    def __init__(self, x, y, sx, sy, player):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.outline_rect = pygame.Rect(x-1, y-1, sx+2, sy+2)
        self.bottom_rect = pygame.Rect(x, y, sx, sy)
        self.top_rect = pygame.Rect(x, y, 0, sy)

        self.player = player

    def update(self, delta):
        self.top_rect.width = self.player.charge / self.player.charge_max * self.sx


    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('black'), self.outline_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.bottom_rect)
        pygame.draw.rect(screen, (0, 255, 0), self.top_rect)