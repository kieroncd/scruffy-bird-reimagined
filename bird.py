import pygame


class Bird:

    def __init__(self, ability=None, name="joe"):
        self.x = 100
        self.y = 150
        self.v = 0
        self.name = name
        self.ability = ability
        self.sprite = pygame.image.load(f'graphics/{name}.png').convert_alpha()
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

        self.charge = 0
        self.charge_max = 100
        self.charge_rate = 20

    def update(self, delta, world_state):
        self.v += world_state.state['gravity'] * delta
        self.y += self.v
        self.rect = self.sprite.get_rect(center=(100, self.y))
        self.charge = min(self.charge + self.charge_rate * delta, self.charge_max)

    def render(self, screen):
        screen.blit(self.sprite, self.rect)

    def reset(self):
        self.x = 100
        self.y = 150
        self.v = 0
        self.charge = 0

    def process_input(self, events):
        # TODO: implement fixed timestep impulse (no idea what I meant by this)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_SPACE]:
                    self.v = -4
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.v = -4