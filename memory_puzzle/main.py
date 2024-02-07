import pygame, sys, os, random

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
    def __init__(self, left, top, width, height, face):
        super().__init__(left, top, width, height)
        self.color = COVER_WHITE
        self.face = face 
        self.reveal = False
        
    def draw(self, surface):
        if not self.reveal:
            pygame.draw.rect(surface, self.color, self)
        else:
            x, y = self.left, self.top
            x += self.face.get_width() / 2
            y += self.face.get_height() / 2
            surface.blit(self.face, (x, y))
    
    def checkReveal(self):
        x, y = pygame.mouse.get_pos()
        self.reveal = self.collidepoint(x, y)

def loadShapes():
    shapes = []
    for filename in os.listdir("assets"):
        filepath = os.path.join("assets", filename)
        image = pygame.image.load(filepath)
        image = image.convert()
        original_width, original_height = image.get_width(), image.get_height()
        # Scale up the image
        scale_factor = 1.4  # Change the scale factor as desired
        image = pygame.transform.scale(image, (original_width * scale_factor, original_height * scale_factor))
        image.set_colorkey((0, 0, 0))
        shapes.append(image)
    return shapes

def getLeftTop(row, col):
    return (SPACE_X + col * CELL_SIZE + GAP * col, SPACE_Y + row * CELL_SIZE + GAP * row) 

def makeGrid(nrow, ncol, shapes):
    grid = []
    pos = []
    for row in range(nrow):
        for col in range(ncol):
            pos.append((row, col))
    random.shuffle(pos)
    random.shuffle(shapes)
    while pos:
        row, col = pos.pop()
        row2, col2 = pos.pop()
        face = shapes.pop()
        box = Box(*getLeftTop(row, col), CELL_SIZE, CELL_SIZE, face)
        box2 = Box(*getLeftTop(row2, col2), CELL_SIZE, CELL_SIZE, face)
        grid.extend([box, box2])
    return grid 

def drawGrid(grid, screen):
    for box in grid:
        box.draw(screen)

def checkMouseReveal(grid):
    for box in grid:
        box.checkReveal()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    shapes = loadShapes()
    grid = makeGrid(GRID_ROW, GRID_COL, shapes)
    while True:
        screen.fill(DARK_GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
        checkMouseReveal(grid)
        drawGrid(grid, screen)
        pygame.display.update()
        clock.tick(FPS)
                




if __name__ == "__main__":
    main()