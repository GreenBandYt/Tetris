import pygame
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tetris")


# Загрузите изображение и получите его размеры
image = pygame.image.load('zerocat.png')
image_height = image.get_height()

# Начальные параметры
visible_image_height = 0
line_height = 30  # Высота строки в тетрисе


done = False
clock = pygame.time.Clock()

class Shape:

        def __init__(self):
            self.x = size[0] // 40
            self.y = 0
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.blocks = []

        def move_down(self, grid):

            if self.y + len(self.blocks) >= len(grid):
               return False
            for i, row in enumerate(self.blocks):
                for j, val in enumerate(row):
                    if val and grid[self.y + i + 1][self.x + j]:
                        return False
            self.y += 1
            return True

        def move_side(self, dx, grid):
            if self.x + dx < 0 or self.x + len(self.blocks[0]) + dx > len(grid[0]):
                return False
            for i, row in enumerate(self.blocks):
                for j, val in enumerate(row):
                    if val and grid[self.y + i][self.x + j + dx]:
                        return False
            self.x += dx
            return True

        def rotate(self, grid):
            new_blocks = [list(reversed(x)) for x in zip(*self.blocks)]
            new_x = self.x
            new_y = self.y
            if new_x + len(new_blocks[0]) > len(grid[0]):
                new_x = len(grid[0]) - len(new_blocks[0])
            if new_y + len(new_blocks) > len(grid):
                new_y = len(grid) - len(new_blocks)
            for i, row in enumerate(new_blocks):
                for j, val in enumerate(row):
                    if val and grid[new_y + i][new_x + j]:
                        return False
            self.blocks = new_blocks
            self.x = new_x
            self.y = new_y
            return True

class I_Shape(Shape):

    def __init__(self):
            super().__init__()
            self.blocks = [[1, 1, 1, 1]]

class J_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[1, 0, 0], [1, 1, 1]]

class L_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[0, 0, 1], [1, 1, 1]]

class O_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[1, 1], [1, 1]]

class S_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[0, 1, 1], [1, 1, 0]]

class T_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[0, 1, 0], [1, 1, 1]]

class Z_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[1, 1, 0], [0, 1, 1]]

shapes = [I_Shape, J_Shape, L_Shape, O_Shape, S_Shape, T_Shape, Z_Shape]

grid = [[0 for _ in range(size[0] // 20)] for _ in range(size[1] // 20)]
shape = random.choice(shapes)()

def clear_rows(grid):
    new_grid = [row for row in grid if not all(row)]
    while len(new_grid) < len(grid):
        new_grid.insert(0, [0 for _ in range(len(grid[0]))])
    return new_grid

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shape.move_side(-1, grid)
            elif event.key == pygame.K_RIGHT:
                shape.move_side(1, grid)
            elif event.key == pygame.K_DOWN:
                shape.move_down(grid)
            elif event.key == pygame.K_UP:
                shape.rotate(grid)

    screen.fill(black)
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, white, [j * 20, i * 20, 20, 20], 0)

    for i, row in enumerate(shape.blocks):
        for j, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, shape.color, [(shape.x + j) * 20, (shape.y + i) * 20, 20, 20], 0)

    if not shape.move_down(grid):
        for i, row in enumerate(shape.blocks):
            for j, val in enumerate(row):
                if val:
                    grid[shape.y + i][shape.x + j] = 1
        grid = clear_rows(grid)
        shape = random.choice(shapes)()

    pygame.display.flip()
    clock.tick(2) # Скорость падения

pygame.quit()