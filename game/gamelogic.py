import os
import random
import sys

import pygame
from loguru import logger

from game.items import Segment, Food
from game.rays import SnakeRay
from game.settings import *

# Текстуры для игры
SEGMENT = pygame.transform.scale(pygame.image.load(os.path.join(f"{os.getcwd()}/game/textures/segment.png")), (BLOCKS_SIZE, BLOCKS_SIZE))
HEAD = pygame.transform.scale(pygame.image.load(os.path.join(f"{os.getcwd()}/game/textures/head.png")), (BLOCKS_SIZE, BLOCKS_SIZE))
FOOD = pygame.transform.scale(pygame.image.load(os.path.join(f"{os.getcwd()}/game/textures/food.png")), (BLOCKS_SIZE, BLOCKS_SIZE))

# Создаем окно и задаем ему название.
screen = pygame.display.set_mode(size=WINDOW_SIZE)
pygame.display.set_caption("AI Snake")
# Таймер тиков.
timer = pygame.time.Clock()


# Переводим координаты клеток в позицию на экране.
def conv_cords(grid_row, grid_column):
    return [
        BLOCKS_SIZE + grid_column * BLOCKS_SIZE,
        (WINDOW_SIZE[1] / 2 - (BLOCKS_COUNT * BLOCKS_SIZE / 2)) + grid_row * BLOCKS_SIZE,
        BLOCKS_SIZE, BLOCKS_SIZE
    ]


"""======================================
        Функции отрисовки объектов.
======================================"""


# Рисуем фоновую клетку.
def draw_cell(color, grid_row, grid_column):
    position = conv_cords(grid_row, grid_column)
    pygame.draw.rect(screen, color, position)


# Рисуем сегмент змейки.
def draw_snake(snake_texture, grid_row, grid_column, segment_rotation=0):
    position = conv_cords(grid_row, grid_column)
    screen.blit(pygame.transform.rotate(snake_texture, segment_rotation), position)


def draw_food(food_obj, grid_row, grid_column):
    position = conv_cords(grid_row, grid_column)
    screen.blit(food_obj, position)


"""======================================
            Игровые переменные.
======================================"""
# Еда.
food = Food()

# Список сегментов змейки.
reset_snake = [Segment(3, 1, 90), Segment(3, 1, 90), Segment(3, 1, 90)]
snake_blocks = [Segment(3, 1, 90), Segment(3, 1, 90), Segment(3, 1, 90)]

# Позиция головы
d_row = 0
d_col = 1

# Рейкасты
ray_x, ray_nx = SnakeRay(1, 0), SnakeRay(-1, 0)
ray_y, ray_ny = SnakeRay(0, 1), SnakeRay(0, -1)

"""-----------------------------------"""


# Управление.
def set_move_direction(direction):
    if direction == 'UP':
        return -1, 0
    elif direction == 'DOWN':
        return 1, 0
    elif direction == 'LEFT':
        return 0, -1
    elif direction == 'RIGHT':
        return 0, 1
    else:
        return d_row, d_col


"""======================================
              Главный цикл.
======================================"""
# Количество попыток.
episodes = 5

for episode in range(1, episodes + 1):
    done = False
    score = 0

    while True:
        # Проходимся по всем ивентам.
        for event in pygame.event.get():
            # Выходим, если нажата кнопка выхода.
            if event.type == pygame.QUIT:
                pygame.quit()
                logger.debug("Сompletion.")
                sys.exit()

            # Управление змейкой
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    d_row = -1
                    d_col = 0
                    logger.debug('Up')
                if event.key == pygame.K_DOWN and d_col != 0:
                    d_row = 1
                    d_col = 0
                    logger.debug('Down')
                if event.key == pygame.K_LEFT and d_row != 0:
                    d_row = 0
                    d_col = -1
                    logger.debug('Left')
                if event.key == pygame.K_RIGHT and d_row != 0:
                    d_row = 0
                    d_col = 1
                    logger.debug('Right')

        """======================================
                      Графика игры.
        ======================================"""
        # Заполняем фон цветом.
        screen.fill(FRAME_COLOR)

        # Размечаем поле на клетки.
        for row in range(BLOCKS_COUNT):
            for column in range(BLOCKS_COUNT):
                # Рисуем только каждую вторую клетку.
                if (row + column) % 2 == 0:
                    continue
                # Рисуем эти самые квадраты.
                draw_cell(BLOCK_COLOR, row, column)

        # Рисуем фрукт.
        draw_food(FOOD, food.x, food.y)

        # Отрисовываем сегменты змейки из списка
        for block in snake_blocks:
            texture = HEAD if block.head else SEGMENT
            draw_snake(texture, block.x, block.y, block.rotation)

        """======================================
             Логика движения, сметри награды.
        ======================================"""

        # Получаем голову (Она всегда является последним элементом).
        head = snake_blocks[-1]

        # logger.debug(f"d_c: {d_col}, d_r: {d_row}")
        # logger.debug(f"X: {ray_x.check(head)} | -X: {ray_nx.check(head)}")
        # logger.debug(f"Y: {ray_y.check(head)} | -Y: {ray_ny.check(head)}")
        # print('\n')
        """-----------------------------------"""
        # Случайные действия, предпринимаемые ИИ.
        action = random.choice(["NOPE", "UP", "DOWN", "LEFT", "RIGHT"])
        d_row, d_col = set_move_direction(action)
        """-----------------------------------"""
        # Проверяем коллизию со стеной. Перезапускаем игру,
        # если змейка ушла за пределы.
        if not head.is_inside():
            snake_blocks.clear()
            for i in reset_snake:
                snake_blocks.append(i)
            head = snake_blocks[-1]
            d_row, d_col = 0, 1
            food = Food()
            logger.info("Game Over!")
            break

        # Проверка на получение еды. Если позиция головы = еде.
        if food.check_snake(head):
            snake_blocks.insert(0, snake_blocks[0])
            food = Food()
            score += 1
        """-----------------------------------"""
        # Создаём новую, с нужным смещением и добавляем в список сегментов змейки.
        rotation = 90 if d_row == 0 else 0
        new_head = Segment(head.x + d_row, head.y + d_col, rotation)
        snake_blocks.append(new_head)
        # Удаляем последнюю клетку
        snake_blocks.pop(0)
        """-----------------------------------"""
        # Отрисовываем всё, что создавали. Задаем тики.
        pygame.display.flip()
        timer.tick(TICK_SPEED)

    print(f"Episode: {episode}, Score: {score}")
