import pygame

class ScrollText:

    def __init__(self, x, y, text):
        self.rect = pygame.Rect((x, y), (0,0 ))
        self.font = pygame.font.SysFont("Agency FB", 20)
        self.color = (255, 255, 255)
        self.scroll = 0

        lines = wrap_text(text, self.font, self.rect.width)

        self.line_surfaces = [self.font.render(line, True, self.color) for line in lines]
        self.line_height = self.font.get_linesize()

        self.content_height = len(self.line_surfaces) * self.line_height

    def process_input(self, events, scene):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                scene.change_scene(scene.next)

    def render(self, screen):

        clip = screen.get_clip()
        screen.set_clip(self.rect)

        y = self.rect.y - self.scroll

        for surf in self.line_surfaces:
            screen.blit(surf, (self.rect.x, y))
            y += self.line_height

        screen.set_clip(clip)

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current = ""

    for word in words:
        test = current + word + " "
        if font.size(test)[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word + " "

    lines.append(current)
    return lines


shitpost = "You open the game and there I am — not a bird, not feathers, not wings — just a picture of me, \
a scruff, floating where a bird should be, and the sky behind me isn’t really a sky at all, it’s pixel art \
of university life. Pixel lecture halls and pixel laptops and pixel coffee cups stacked like tiny monuments \
to late nights, and you see it and you think it’s just a joke and maybe it is, but you keep watching. You \
tap the screen and scruff rises a little and the pixels shake slightly and the world scrolls left like time \
does in university, like everything moving forward whether you’re ready or not. Pipes appear — tall red \
and yellow things that look suspiciously like ketchup and mayo packets and deadlines — and you try to slip \
between them and you almost make it and you tell yourself the next one will be easier. And there’s something \
weirdly personal about it because the background keeps changing and suddenly you’re flying past a pixel dorm \
room and then a lab and then a glowing laptop screen where something actually happened once, something small \
but important: my first ever pull request. You wouldn’t notice it if you blinked — just a tiny pixel window \
of code — but it’s there and there’s a bug in the program and there’s me staring at it too long and there’s \
the moment the fix finally clicks and I push the change and open the pull request like it’s a message in a \
bottle sent into the ocean of the internet. And scruff keeps flying and the pixels keep sliding past and the \
game doesn’t really end so much as continue until you mess up, which you will, because that’s how these games \
work and that’s how university works too: you keep tapping and adjusting and learning the rhythm of things \
and sometimes you hit the pipe and sometimes you make it through and once in a while you fix a bug and send \
your first pull request and realize you’re actually part of the system now."

st = ScrollText(0, 0,  shitpost)
print(st.lines)