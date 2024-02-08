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
    def __init__(self, left, top, width, height, face, idx):
        super().__init__(left, top, width, height)
        self.color = COVER_WHITE
        self.face = face 
        self.reveal = False
        self.permanent = False 
        self.idx = idx
        
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
    
    def __eq__(self, other):
        return self.idx == other.idx

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
    idx = 0
    while pos:
        row, col = pos.pop()
        row2, col2 = pos.pop()
        face = shapes.pop()
        box = Box(*getLeftTop(row, col), CELL_SIZE, CELL_SIZE, face, idx)
        box2 = Box(*getLeftTop(row2, col2), CELL_SIZE, CELL_SIZE, face, idx)
        grid.extend([box, box2])
        idx += 1
    return grid 

def drawGrid(grid, screen):
    for box in grid:
        box.draw(screen)

def checkMouseReveal(grid):
    pair = []
    for i, box in enumerate(grid):
        grid[i].checkReveal()
        if grid[i].reveal and not grid[i].permanent:
            pair.append([grid[i], i])
    return pair

def gridCheck(grid, timer, dt, pair):
    if timer["active"]:
        timer["time"] += dt / 1000
        if timer["time"] > WAIT_TIME:
            timer["time"] = 0
            timer["active"] = False
    else:
        if len(pair) == 2:
            timer["active"] = True
            if pair[0][0] == pair[1][0]:
                index_1, index_2 = pair[0][1], pair[1][1]
                grid[index_1].permanent = True
                grid[index_2].permanent = True
            else:
                index_1, index_2 = pair[0][1], pair[1][1]
                grid[index_1].reveal = False
                grid[index_2].reveal = False
            pair = []

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Memory Game")
    clock = pygame.time.Clock()
    shapes = loadShapes()
    grid = makeGrid(GRID_ROW, GRID_COL, shapes)
    pair = [] # store the two revealed boxes
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
                pair = checkMouseReveal(grid)
        gridCheck(grid, timer, dt, pair)
        drawGrid(grid, screen)
        pygame.display.update()
        dt = clock.tick(FPS)
                


if __name__ == "__main__":
    main()