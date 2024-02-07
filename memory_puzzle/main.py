import pygame, sys

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
DARK_GREEN = (2, 48, 32)
COVER_WHITE = (200, 200, 200)
FPS = 60
CELL_SIZE = 60
GAP = 10
SPACE_X = 250
SPACE_Y = 150
GRID_ROW = 4
GRID_COL = 4

class Box(pygame.Rect):
    def __init__(self, left, top, width, height):
        super().__init__(left, top, width, height)
        self.color = COVER_WHITE
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)

def getLeftTop(row, col):
    return (SPACE_X + col * CELL_SIZE + GAP * col, SPACE_Y + row * CELL_SIZE + GAP * row) 

def makeGrid(nrow, ncol):
    grid = []
    for row in range(nrow):
        for col in range(ncol):
            box = Box(*getLeftTop(row, col), CELL_SIZE, CELL_SIZE)
            grid.append(box)
    return grid 

def drawGrid(grid, screen):
    for box in grid:
        box.draw(screen)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    grid = makeGrid(GRID_ROW, GRID_COL)
    while True:
        screen.fill(DARK_GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        drawGrid(grid, screen)
        pygame.display.update()
        clock.tick(FPS)
                




if __name__ == "__main__":
    main()