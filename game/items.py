from loguru import logger
import random

from settings import *


class Segment:
    def __init__(self, x, y, rotation=0, head=False):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.head = head
        # logger.debug("Segment created")

    def is_inside(self):
        return 0 <= self.x < BLOCKS_COUNT and 0 <= self.y < BLOCKS_COUNT


class Food:
    def __init__(self):
        self.x = random.randint(0, BLOCKS_COUNT - 1)
        self.y = random.randint(0, BLOCKS_COUNT - 1)

    def check_snake(self, snake_head):
        if snake_head.x == self.x and snake_head.y == self.y:
            logger.info("Nom!")
            return True
