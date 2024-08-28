import pygame
import random

# Инициализация модуля Pygame
pygame.init()

# Определяем цвета
black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

# Размеры окна игры
size = (400, 500)
screen = pygame.display.set_mode(size)  # Создаем окно
pygame.display.set_caption("Tetris")  # Устанавливаем заголовок окна

# Загрузите изображение и получите его размеры
image = pygame.image.load('zerocat.png')
image_height = image.get_height()

# Начальные параметры
visible_image_height = 0
line_height = 30  # Высота строки в тетрисе

done = False  # Флаг для завершения игры
paused = False  # Флаг для паузы
clock = pygame.time.Clock()  # Создаем объект для отслеживания времени

# Базовый класс для всех фигур
class Shape:
    def __init__(self):
        self.x = size[0] // 40  # Начальная позиция по X
        self.y = 0  # Начальная позиция по Y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Случайный цвет
        self.blocks = []  # Массив для хранения формы фигуры

    # Метод для перемещения фигуры вниз
    def move_down(self, grid):
        if self.y + len(self.blocks) >= len(grid):  # Проверка на дно
            return False
        for i, row in enumerate(self.blocks):
            for j, val in enumerate(row):
                if val and grid[self.y + i + 1][self.x + j]:  # Проверка на столкновение с другой фигурой
                    return False
        self.y += 1  # Перемещение вниз
        return True

    # Метод для перемещения фигуры влево или вправо
    def move_side(self, dx, grid):
        if self.x + dx < 0 or self.x + len(self.blocks[0]) + dx > len(grid[0]):  # Проверка на границы
            return False
        for i, row in enumerate(self.blocks):
            for j, val in enumerate(row):
                if val and grid[self.y + i][self.x + j + dx]:  # Проверка на столкновение
                    return False
        self.x += dx  # Перемещение в сторону
        return True

    # Метод для вращения фигуры
    def rotate(self, grid):
        new_blocks = [list(reversed(x)) for x in zip(*self.blocks)]  # Поворот на 90 градусов
        new_x = self.x
        new_y = self.y
        if new_x + len(new_blocks[0]) > len(grid[0]):  # Проверка на выход за границы
            new_x = len(grid[0]) - len(new_blocks[0])
        if new_y + len(new_blocks) > len(grid):  # Проверка на выход за границы
            new_y = len(grid) - len(new_blocks)
        for i, row in enumerate(new_blocks):
            for j, val in enumerate(row):
                if val and grid[new_y + i][new_x + j]:  # Проверка на столкновение
                    return False
        self.blocks = new_blocks  # Применение нового положения
        self.x = new_x
        self.y = new_y
        return True

# Определяем классы для каждой из фигур тетриса
class I_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[1, 1, 1, 1]]  # Форма I

class J_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[1, 0, 0], [1, 1, 1]]  # Форма J

class L_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[0, 0, 1], [1, 1, 1]]  # Форма L

class O_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[1, 1], [1, 1]]  # Форма O

class S_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[0, 1, 1], [1, 1, 0]]  # Форма S

class T_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[0, 1, 0], [1, 1, 1]]  # Форма T

class Z_Shape(Shape):
    def __init__(self):
        super().__init__()
        self.blocks = [[1, 1, 0], [0, 1, 1]]  # Форма Z

# Список всех фигур
shapes = [I_Shape, J_Shape, L_Shape, O_Shape, S_Shape, T_Shape, Z_Shape]

# Создаем пустую сетку
grid = [[0 for _ in range(size[0] // 20)] for _ in range(size[1] // 20)]
shape = random.choice(shapes)()  # Выбираем случайную фигуру

def freeze_shape(shape, grid):
    for i, row in enumerate(shape.blocks):
        for j, val in enumerate(row):
            if val:
                grid[shape.y + i][shape.x + j] = 1  # Сохраняем фигуру в сетке

def clear_rows(grid):
    new_grid = [row for row in grid if any(val == 0 for val in row)]
    cleared = len(grid) - len(new_grid)
    for _ in range(cleared):
        new_grid.insert(0, [0] * len(grid[0]))
    grid[:] = new_grid
    return cleared

# Основной цикл игры
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
            elif event.key == pygame.K_SPACE:
                paused = not paused

    if not paused:
        if not shape.move_down(grid):
            freeze_shape(shape, grid)
            filled_lines = clear_rows(grid)
            # Обновление видимой части изображения
            if filled_lines > 0:
                visible_image_height += filled_lines * line_height*1 # ДЛЯ ТЕСТИРОВАНИЯ ПОБЕДЫ ПОМЕНЯТЬ НА 20
                if visible_image_height >= image_height:
                    # Остановка игры и отображение поздравления
                    done = True
                    grid = [[0 for _ in range(size[0] // 20)] for _ in range(size[1] // 20)]
                    font = pygame.font.SysFont(None, 35)
                    win_text = font.render("Поздравляем! Вы выиграли!", True, white)
                    screen.blit(win_text,
                                (size[0] // 2 - win_text.get_width() // 2, size[1] // 2 - win_text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(3000)  # Ожидание 10 секунд для показа поздравления

            shape = random.choice(shapes)()

            if not shape.move_down(grid):
                done = True

        # Отрисовка сетки и фигур
        screen.fill(black)

        # Отображение части изображения
        screen.blit(image, (0, size[1] - visible_image_height),
                    (0, image_height - visible_image_height, size[0], visible_image_height))

        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, gray, [j * 20, i * 20, 20, 20], 0)

        for i, row in enumerate(shape.blocks):
            for j, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, shape.color, [(shape.x + j) * 20, (shape.y + i) * 20, 20, 20], 0)

    if paused:
        font = pygame.font.SysFont(None, 75)
        pause_text = font.render("ПАУЗА", True, white)
        screen.blit(pause_text,
                    (size[0] // 2 - pause_text.get_width() // 2, size[1] // 2 - pause_text.get_height() // 2))

    pygame.display.flip()
    clock.tick(3)

pygame.quit()
