import pygame

from ui.outlinetext import OutlinedText


class Button:

    def __init__(self, x, y, sx, sy, alt_button=None, func=None, func_args=None):
        if func_args is None:
            func_args = []
        self.x, self.y = x, y
        self.sx, self.sy = sx, sy
        self.func = func
        self.func_args = func_args
        self.rect = pygame.Rect((x, y), (sx, sy))
        self.outline_rect = pygame.Rect((x-1, y-1), (sx+2, sy+2))
        self.alt_button = alt_button

    def update(self, delta):
        pass

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.outline_rect)
        pygame.draw.rect(screen, (0, 148, 255), self.rect)

    def process_input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.func(*self.func_args)
            if event.type == pygame.KEYDOWN and event.key == self.alt_button:
                self.func(*self.func_args)


class TextButton(Button):

    def __init__(self, x, y, sx, sy, text="", alt_button=None, func=None, func_args=None):
        super().__init__(x, y, sx, sy, alt_button, func, func_args)

        self.text = text

        font = pygame.font.SysFont("Agency FB", 20)
        self.text = font.render(text, False, (255, 216, 0))
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def render(self, screen):
        super().render(screen)
        screen.blit(self.text, self.text_rect)



class CharacterButton(Button):

    def __init__(self, x, y, sx, sy, bird_data, alt_button=None, func=None, func_args=None):
        super().__init__(x, y, sx, sy, alt_button, func, func_args)
        self.bird_data = bird_data

        self.sprite = pygame.image.load(f"graphics/{bird_data['name']}.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (sx, sx))  # keep square sprite

        font = pygame.font.SysFont("Agency FB", 16)
        self.name_text = OutlinedText(
            text=bird_data["name"].capitalize(),
            font=font,
            x=x + sx // 2,
            y=y + sy + 12,          # position just below the button
            colour=(255, 255, 255),
            outlinecolour=(0, 0, 0),
            thick=1
        )

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.outline_rect)
        pygame.draw.rect(screen, (0, 148, 255), self.rect)

        screen.blit(self.sprite, self.rect.topleft)

        self.name_text.render(screen)

    def process_input(self, events):
        super().process_input(events)