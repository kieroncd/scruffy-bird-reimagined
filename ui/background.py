import pygame


class Background:

    def __init__(self, sprite='background', x=0, y=0):
        self.x, self.y = x, y
        self.sprite = pygame.image.load(f'ui/ui-graphics/{sprite}.png').convert()
        self.rect = self.sprite.get_rect(topleft=(x, y))

    def update(self, delta, speed=10):
        self.x -= speed * delta
        self.rect = self.sprite.get_rect(topleft=(self.x, self.y))

    def render(self, screen):
        screen.blit(self.sprite, self.rect)

    def reposition(self, reference_rect):
        if self.rect.topright[0] < 0:
            new_x, new_y = reference_rect.topright
            self.x, self.y = new_x, new_y
            self.rect = self.sprite.get_rect(topleft=(new_x, new_y))


class ScrollingBackground:

    def __init__(self, sprite='background', x=0, y=0, scroll_speed=30):
        self.x, self.y = x, y
        self.scroll_speed = scroll_speed
        self.bg_one = Background(sprite=sprite, x=x, y=y)
        self.bg_two = Background(sprite=sprite, x=self.bg_one.rect.topright[0], y=self.bg_one.rect.topright[1])

    def bg_elements(self):
        return [self.bg_one, self.bg_two]

    def update(self, delta):
        for e in self.bg_elements():
            e.update(delta, self.scroll_speed)
        self.bg_one.reposition(self.bg_two.rect)
        self.bg_two.reposition(self.bg_one.rect)

    def render(self, screen):
        for e in self.bg_elements():
            e.render(screen)
