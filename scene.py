import pygame
import json
from bird import Bird
from pipe import PipePair
from ui.cooldown import CoolDownTimer
from ui.outlinetext import OutlinedText
from ui.uimanager import UIManager
from ui.background import ScrollingBackground, Background
from ui.button import TextButton, CharacterButton
from ui.scorecounter import ScoreCounter
from worldstate import WorldModifier, WorldState


class Scene:

    def __init__(self):
        self.next = self
        self.ui = UIManager()

    def process_input(self, events):
        self.ui.process_input(events)

    def update(self, delta):
        self.ui.update(delta)

    def render(self, screen):
        self.ui.render(screen)

    def switch_scene(self, next_scene):
        self.next = next_scene

    def kill(self):
        self.next = None


class SplashScene(Scene):

    def __init__(self):
        super().__init__()
        self.phase = "animation"
        self.timer = 0

        # timings (seconds)
        self.fade_in_time = 0.5
        self.hold_time = 1
        self.fade_out_time = 0.5
        self.image = pygame.image.load(r'graphics/splash.png').convert_alpha()
        self.rect = self.image.get_rect(center=(125, 150))


        self.font = pygame.font.SysFont("Agency FB", 20)


        shitpost = """You open the game and there I am - not a bird, not feathers, not wings - just a picture of me, 
        a scruff, floating where a bird should be, and the sky behind me isn’t really a sky at all, it’s pixel art of 
        university life. Pixel lecture halls and pixel laptops and pixel coffee cups stacked like tiny monuments to 
        late nights, and you see it and you think it’s just a joke and maybe it is, but you keep watching. You tap the 
        screen and scruff rises a little and the pixels shake slightly and the world scrolls left like time does in 
        university, like everything moving forward whether you’re ready or not. Pipes appear - tall red and yellow 
        things that look suspiciously like ketchup and mayo packets and deadlines - and you try to slip between them 
        and you almost make it and you tell yourself the next one will be easier. And there’s something weirdly 
        personal about it because the background keeps changing and suddenly you’re flying past a pixel dorm room and 
        then a lab and then a glowing laptop screen where something actually happened once, something small but 
        important: my first ever pull request. You wouldn’t notice it if you blinked - just a tiny pixel window of 
        code - but it’s there and there’s a bug in the program and there’s me staring at it too long and there’s the 
        moment the fix finally clicks and I push the change and open the pull request like it’s a message in a bottle 
        sent into the ocean of the internet. And scruff keeps flying and the pixels keep sliding past and the game 
        doesn’t really end so much as continue until you mess up, which you will, because that’s how these games work 
        and that’s how university works too: you keep tapping and adjusting and learning the rhythm of things and 
        sometimes you hit the pipe and sometimes you make it through and once in a while you fix a bug and send your 
        first pull request and realize you’re actually part of the system now."""
        # wrap text
        words = shitpost.split()
        lines = []
        current = ""

        for word in words:
            test = current + word + " "
            if self.font.size(test)[0] <= 250:
                current = test
            else:
                lines.append(current)
                current = word + " "
        lines.append(current)

        # render lines
        self.lines = [self.font.render(line, True, (255, 255, 255)) for line in lines]

        self.line_height = self.font.get_linesize()

        # start below screen
        self.scroll_y = 300

        self.center_x = 125

    def process_input(self, events):
        super().process_input(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.switch_scene(TitleScene())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.switch_scene(TitleScene())

    def update(self, delta, scroll_speed=25):

        self.timer += delta

        if self.phase == "animation":

            total_anim = self.fade_in_time + self.hold_time + self.fade_out_time

            if self.timer >= total_anim:
                self.phase = "scrolling"

        elif self.phase == "scrolling":
            self.scroll_y -= scroll_speed * delta

            text_height = len(self.lines) * self.line_height
            if self.scroll_y + text_height < 0:
                self.switch_scene(TitleScene())

    def render(self, screen):

        if self.phase == "animation":
            self.render_animation(screen)

        elif self.phase == "scrolling":
            self.render_text(screen)


    def render_animation(self, screen):

        t = self.timer

        if t < self.fade_in_time:
            alpha = int(255 * (t / self.fade_in_time))

        elif t < self.fade_in_time + self.hold_time:
            alpha = 255

        else:
            fade_t = t - (self.fade_in_time + self.hold_time)
            alpha = int(255 * (1 - fade_t / self.fade_out_time))

        img = self.image.copy()
        img.set_alpha(alpha)

        screen.blit(img, self.rect)


    def render_text(self, screen):

        for i, surf in enumerate(self.lines):

            y = self.scroll_y + i * self.line_height
            rect = surf.get_rect(center=(self.center_x, y))

            screen.blit(surf, rect)


class TitleScene(Scene):

    def __init__(self, player=None, background=None):
        super().__init__()

        self.logo = pygame.image.load(r'ui/ui-graphics/logo.png').convert_alpha()
        self.background = background or ScrollingBackground(scroll_speed=50)
        if player is not None:
            self.player = player
        else:
            self.player = Bird(name="joe", ability=WorldModifier("pipe_speed", 50, 1000))

        self.ui.add("start",
            TextButton(
                50, 150, 150, 20,
                "Start",
                alt_button=pygame.K_SPACE,
                func=lambda: self.switch_scene(LevelScene(WorldState(), self.player, self.background))
            )
        )
        self.ui.add("charselect",
            TextButton(
                50, 200, 150, 20,
                "Pick Bird",
                func=lambda: self.switch_scene(CharacterSelectScene(self.background))
            )
        )

    def update(self, delta):
        self.background.update(delta)
        super().update(delta)

    def render(self, screen):
        self.background.render(screen)
        screen.blit(self.logo, self.logo.get_rect(topleft=(50, 20)))
        screen.blit(self.player.sprite, self.player.sprite.get_rect(center=(125, 120)))
        super().render(screen)


class LevelScene(Scene):

    def __init__(self, world_state, player=None, background=None):
        super().__init__()

        if player is not None:
            self.player = player
        else:
            self.player = Bird(ability=WorldModifier("pipe_speed", 50, 1000))
        self.pipe_one = PipePair(300)
        self.pipe_two = PipePair(500)
        self.world_state = world_state

        self.background = background or ScrollingBackground(x=-745)

        self.entities = [self.pipe_one, self.pipe_two, self.player]
        self.pipes = [self.pipe_one, self.pipe_two]

        self.ui.add("score_counter", ScoreCounter())
        self.ui.add("cooldown", CoolDownTimer(
            10, 20, 100, 15, self.player
        ))

        self.score = 0

    def update(self, delta):
        for e in self.entities:
            e.update(delta, self.world_state)

        if self.world_state.state["powerup"]:
            if pygame.time.get_ticks() > self.world_state.state["expires"]:
                self.world_state.remove_modifier(self.player.ability)

        self.background.update(delta)
        self.check_collisions()
        self.reposition_obstacles()
        self.ui.update(delta)
        self.score = self.ui.get("score_counter").score

    def process_input(self, events):
        self.player.process_input(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_x] and self.player.charge >= self.player.charge_max:
                    self.world_state.add_modifier(self.player.ability)
                    self.player.charge = 0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if self.player.charge >= self.player.charge_max:
                    self.world_state.add_modifier(self.player.ability)
                    self.player.charge = 0
        super().process_input(events)

    def render(self, screen):
        self.background.render(screen)
        for e in self.entities:
            e.render(screen)
        super().render(screen)

    def check_collisions(self):
        # if player is out of bounds, game over
        if self.player.rect.y > 300 or self.player.rect.y < -50:
            self.switch_scene(GameOverScene(self))

        for pipe in self.pipes:
            # checks collision of player with pipes
            if self.player.rect.colliderect(pipe.upper.rect) or self.player.rect.colliderect(pipe.lower.rect):
                self.switch_scene(GameOverScene(self))
                return
            # score incrementation
            if pipe.x < self.player.x and pipe.award_points:
                self.ui.get("score_counter").add_score()
                pipe.award_points = False

    def reposition_obstacles(self):
        # once pipes off-screen (left), reposition to "spawn" the next
        if self.pipe_one.check_oob():
            self.pipe_one.reposition(self.pipe_two.x + 200)
        if self.pipe_two.check_oob():
            self.pipe_two.reposition(self.pipe_one.x + 200)


class GameOverScene(Scene):

    def __init__(self, level_scene):
        super().__init__()

        self.player = level_scene.player
        self.player.reset()
        self.background = level_scene.background
        self.score = level_scene.score

        self.background.scrolling_speed = 0

        with open("config.json", "r") as file:
            self.data = json.load(file)

        self.hs = self.data["high-score"]

        if self.score > self.hs:
            self.hs = self.score
            self.data["high-score"] = self.score
            with open("config.json", "w") as file:
                json.dump(self.data, file)

        self.font = pygame.font.SysFont("Agency FB", 24)

        self.text = [
            OutlinedText("Game Over!", self.font, x=125, y=125),
            OutlinedText(f"Score: {self.score}", self.font, x=125, y=150),
            OutlinedText(f"High Score: {self.hs}", self.font, x=125, y=175)
        ]

        self.ui.add(
            "mainmenu",
            TextButton(
                50, 275, 150, 20,
                "Main Menu",
                pygame.K_SPACE,
                lambda: self.switch_scene(TitleScene(self.player, self.background))
            )
        )

    def update(self, delta):
        self.ui.update(delta)

    def render(self, screen):
        self.background.render(screen)

        for t in self.text:
            t.render(screen)

        self.ui.render(screen)


class CharacterSelectScene(Scene):

    def __init__(self, background=None):
        super().__init__()
        self.background = background or ScrollingBackground(scroll_speed=50)

        self.available_birds = [
            {"name": "joe", "ability": WorldModifier("pipe_speed", 50, 1000)},
            {"name": "kieron", "ability": WorldModifier("gravity", 5, 1000)},
            {"name": "gibbons", "ability": WorldModifier("pipe_speed", 50, 1000)},
            {"name": "theo", "ability": WorldModifier("pipe_speed", 50, 1000)}
        ]
        self.background = background or ScrollingBackground(scroll_speed=50)
        self.selected_bird = None
        self.generate_buttons()

    def generate_buttons(self):
        x_i = 60
        y_i = 60
        padding_x = 80
        padding_y = 120
        num_x = 2
        num_y = 2

        for i in range(num_y):
            for j in range(num_x):
                idx = i * num_x + j
                bird_data = self.available_birds[idx]
                x = x_i + j * padding_x
                y = y_i + i * padding_y

                btn = CharacterButton(
                    x=x,
                    y=y,
                    sx=50,
                    sy=50,
                    bird_data=bird_data,
                    func=self.select_bird,
                    func_args=[bird_data]
                )
                self.ui.add(f"bird_{idx}", btn)

    def select_bird(self, bird_data):
        self.selected_bird = Bird(name=bird_data["name"], ability=bird_data["ability"])
        self.switch_scene(TitleScene(self.selected_bird, self.background))

    def render(self, screen):
        self.background.render(screen)
        super().render(screen)

    def update(self, delta):
        self.background.update(delta)
        super().update(delta)

