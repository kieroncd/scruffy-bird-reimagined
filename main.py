import pygame
from scene import SplashScene


def run_game():
    pygame.init()
    pygame.display.set_caption("Scruffy Bird Reimagined")
    screen = pygame.display.set_mode((250, 300))
    clock = pygame.time.Clock()
    scene = SplashScene()

    while scene is not None:
        fil_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene.kill()
            else:
                fil_events.append(event)
        delta = clock.tick(60) / 1000
        screen.fill((0, 0, 0))
        scene.process_input(fil_events)
        scene.update(delta)
        scene.render(screen)
        scene = scene.next
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    run_game()
