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
WAIT_TIME = 2 # the amount of seconds to show the pair of fruits

class Box(pygame.Rect):
    def __init__(self, left, top, width, height, face):
        super().__init__(left, top, width, height)
        self.color = COVER_WHITE
        self.face = face 
        self.reveal = False
        self.permanent = False 
        
    def draw(self, surface):
        if not self.reveal and not self.permanent:
            pygame.draw.rect(surface, self.color, self)
        else:
            x, y = self.left, self.top
            x += self.face.get_width() / 2
            y += self.face.get_height() / 2
            surface.blit(self.face, (x, y))
    
    def checkReveal(self):
        #if not self.permanent:
        x, y = pygame.mouse.get_pos()
        if not self.reveal:
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
    for i, box in enumerate(grid):
        grid[i].checkReveal()
    return grid 

def checkMatch(grid, timer):
    for i, box in enumerate(grid):
        if box.reveal:
            for j, box2 in enumerate(grid):
                if i != j and box2.reveal:
                    if box.face == box2.face:
                        grid[i].permanent = True
                        grid[j].permanent = True
                        timer["active"] = True
                        return grid, timer
                    else:
                        grid[i].reveal = False
                        grid[j].reveal = False
                        timer["active"] = True
                        return grid, timer
    #timer["active"] = False
    return grid, timer

def gridCheck(grid, timer, dt):
    if timer["active"]:
        timer["time"] += dt / 1000
        if timer["time"] > WAIT_TIME:
            print('close', timer["time"])
            timer["time"] = 0
            timer["active"] = False
    else:
        grid, timer = checkMatch(grid, timer)
    return grid, timer

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    shapes = loadShapes()
    grid = makeGrid(GRID_ROW, GRID_COL, shapes)
    dt = clock.tick(FPS)
    timer = {"time": 0, "active": False} 
    while True:
        screen.fill(DARK_GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                grid = checkMouseReveal(grid)
        grid, timer = gridCheck(grid, timer, dt)
        drawGrid(grid, screen)
        pygame.display.update()
        dt = clock.tick(FPS)
                


if __name__ == "__main__":
    main()