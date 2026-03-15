class OutlinedText:
    def __init__(self, text, font, x=0, y=0, colour=(255,255,255), outlinecolour=(0,0,0), thick=1):
        self.x, self.y = x, y
        self.font = font
        self.colour = colour
        self.outlinecolour = outlinecolour
        self.text = text
        self.thick = thick

        # Render once
        self.text_render = self.font.render(self.text, False, self.colour)
        self.outlinetext = self.font.render(self.text, False, self.outlinecolour)
        self.outlinerect = self.generate_outline_rect()
        self.text_rect = self.text_render.get_rect(center=(self.x, self.y))

    def generate_outline_rect(self):
        rects = []
        for dx in range(-self.thick, self.thick + 1):
            for dy in range(-self.thick, self.thick + 1):
                if dx == 0 and dy == 0:
                    continue
                rects.append(self.outlinetext.get_rect(center=(self.x + dx, self.y + dy)))
        return rects

    def set_text(self, new_text):
        if new_text != self.text:
            self.text = new_text
            self.text_render = self.font.render(self.text, False, self.colour)
            self.outlinetext = self.font.render(self.text, False, self.outlinecolour)
            self.outlinerect = self.generate_outline_rect()
            self.text_rect = self.text_render.get_rect(center=(self.x, self.y))

    def set_colour(self, colour):
        if colour != self.colour:
            self.colour = colour
            self.text_render = self.font.render(self.text, False, self.colour)

    def set_outline_colour(self, outlinecolour):
        if outlinecolour != self.outlinecolour:
            self.outlinecolour = outlinecolour
            self.outlinetext = self.font.render(self.text, False, self.outlinecolour)
            self.outlinerect = self.generate_outline_rect()

    def update(self, delta):
        # Only needed if text moves dynamically
        self.text_rect.center = (self.x, self.y)
        # outline rects follow text
        self.outlinerect = self.generate_outline_rect()

    def render(self, screen):
        for rect in self.outlinerect:
            screen.blit(self.outlinetext, rect)
        screen.blit(self.text_render, self.text_rect)