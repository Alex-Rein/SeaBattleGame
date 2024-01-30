# Внутренняя логика игры — корабли,
# игровая доска и вся логика связанная с ней.

import Exceptions

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'{self.x}, {self.y}'


class Ship:
    def __init__(self, length, head_dot, direction, life):
        self.length = length
        self.head_dot = head_dot
        self.direction = direction
        self.life = life

    def dots(self):
        dot_list = [self.head_dot]
        for i in range(1, self.length):
            if self.direction == 'vertical':
                dot_list.append(Dot(self.head_dot.x, self.head_dot.y + i))
            elif self.direction == 'horizontal':
                dot_list.append(Dot(self.head_dot.x + i, self.head_dot.y))
            else:
                raise


