from .settings import *


class SnakeRay:
    def __init__(self, x_dir, y_dir):
        self.x_dir = x_dir
        self.y_dir = y_dir

    def check(self, head):
        check_x, check_y = head.x, head.y

        if self.x_dir == 1:
            return BLOCKS_COUNT - check_x - 1
        elif self.x_dir == -1:
            return BLOCKS_COUNT - (BLOCKS_COUNT - check_x)

        elif self.y_dir == 1:
            return BLOCKS_COUNT - check_y - 1
        elif self.y_dir == -1:
            return BLOCKS_COUNT - (BLOCKS_COUNT - check_y)
