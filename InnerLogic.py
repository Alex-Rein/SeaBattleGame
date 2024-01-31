# Внутренняя логика игры — корабли,
# игровая доска и вся логика связанная с ней. ■

from Exceptions import *


class Dot:
    _is_busy = False
    _char = 'O'

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other.vals[0] and self._y == other.vals[1]

    def __str__(self):
        return f'{self._x}, {self._y}'

    @property
    def is_busy(self):
        return self._is_busy

    @is_busy.setter
    def is_busy(self, value=bool):
        self._is_busy = value

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, value=str):
        if value == any(['X', 'T', 'O', '■']):
            self._char = value

    @property
    def vals(self):
        """Вывод координат точки в виде кортежа (x, y)"""
        return self._x, self._y


class Ship:
    def __init__(self, head_dot, length, direction):
        self._length = length
        self._head_dot = head_dot
        self._direction = direction
        self._life = length

    def dots(self):
        """Возвращает список всех точек (Dot) корабля"""
        dot_list = [self._head_dot]
        for i in range(1, self._length):
            if self._direction:
                dot_list.append(Dot(self._head_dot.vals[0], self._head_dot.vals[1] + i))
            else:
                dot_list.append(Dot(self._head_dot.vals[0] + i, self._head_dot.vals[1]))
        return dot_list

    def damage(self):
        self._life -= 1

    def get_head_dot(self):
        return self._head_dot

    def get_direction(self):
        return self._direction


class Board:
    _board_status = [[], [], [], [], [], []]
    _fleet_list = []
    _hid = True
    _ships_count = 0

    def __init__(self):
        for row in self._board_status:
            for i in range(6):
                row.append(Dot(i, row))

    def add_ship(self, length):
        print(f'Ставим корабль длины {length}')  # Собираем данные для создания корабля
        while True:  # Цикл для проверки ввода координат
            coords = input('Укажите координаты точки размещения через пробел: ').split()
            if coords[0].isdigit() and coords[1].isdigit():
                coords = list(map(int, coords))
                if coords[0] in range(1, 7) and coords[1] in range(1, 7):  # Проверка диапазона
                    head_dot = Dot(int(coords[0]), int(coords[1]))
                    break
                else:
                    raise BoardOutException(Dot(int(coords[0]), int(coords[1])))
            else:
                raise TypeError('Неправильно указаны координаты')
        direction = input('Корабль ставим вертикально? Y/N  ').lower()
        direction = True if direction == any(['y', 'да', '1']) else False
        ship = Ship(head_dot, length, direction)

        try:  # Пробуем разместить корабль по указанным координатам
            for cell in ship.dots():
                pass  # НУЖЕН МЕТОД ДЛЯ ОБВОДКИ CONTOUR
        except ShipPlacementError:
            return
        else:
            self._fleet_list.append(ship)
            self._ships_count += 1

    def contour(self, ship):
        contour_list = []
        for cell in ship.dots():
            x_y = cell.vals  # координаты текущей точки сокращенно
            for y in range(x_y[1] - 1, x_y[1] + 2):  # Обходим все соседние точки
                if y not in range(1, 7):
                    continue

                for x in range(x_y[0] - 1, x_y[0] + 2):
                    if x not in range(1, 7):
                        continue

                    if x_y != (x, y):   # ПЕРЕДЕЛАТЬ КОД, ДУБЛИРУЮТСЯ ТОЧКИ !!!
                        contour_list.append(Dot(x, y))
        return contour_list

