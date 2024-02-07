import pygame, sys

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
DARK_GREEN = (2, 48, 32)
FPS = 60

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    while True:
        screen.fill(DARK_GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        pygame.display.update()
        clock.tick(FPS)
                




if __name__ == "__main__":
    main()