# Внутренняя логика игры — корабли,
# игровая доска и вся логика связанная с ней.

import Exceptions


class Dot:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    def __str__(self):
        return f'{self._x}, {self._y}'

    def get_dot(self):
        return self._x, self._y


class Ship:
    def __init__(self, length, head_dot, direction):
        self._length = length
        self._head_dot = head_dot
        self._direction = direction
        self._life = length

    def dots(self):
        dot_list = [self._head_dot]
        for i in range(1, self._length):
            if self._direction == 'vertical':  # ПЕРЕДЕЛАТЬ ЧЕРЕЗ boolean
                dot_list.append(Dot(self._head_dot.x, self._head_dot.y + i))
            elif self._direction == 'horizontal':
                dot_list.append(Dot(self._head_dot.x + i, self._head_dot.y))
            else:
                raise Exceptions.ShipDirectionError(self._direction)

    def get_damage(self):
        self._life -= 1

    def get_head_dot(self):
        return self._head_dot

    def get_direction(self):
        return self._direction


class Board:
    _status = [[], [], [], [], [], []]
    _ships_list = []
    _hid = True
    _ships_count = None

    def __init__(self):
        for row in self._status:
            for i in range(6):
                row.append('O')

    def add_ship(self, length, dot, direction):
        ...
