# Внутренняя логика игры — корабли,
# игровая доска и вся логика связанная с ней. ■

from Exceptions import *


class Dot:
    _is_free = True
    _char = 'O'

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other.vals[0] and self._y == other.vals[1]

    def __str__(self):
        return f'{self._x}, {self._y}'

    @property
    def is_free(self):
        return self._is_free

    @is_free.setter
    def is_free(self, value=bool):
        self._is_free = value

    @property
    def char(self):
        return self._char

    @char.setter
    def char(self, value=str):
        if any([value == x for x in ['X', 'T', 'O', '■']]):
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

    def damage(self, dot):
        if dot.char == '■':
            dot.char = 'X'
            self._life -= 1

    def get_head_dot(self):  # НУЖНО ЛИ?
        return self._head_dot

    def get_direction(self):  # НУЖНО ЛИ?
        return self._direction


class Board:
    _board_status = [[], [], [], [], [], []]
    _fleet_list = []
    _ships_count = 0

    def __init__(self, hidden=False):
        self._hid = hidden
        x, y = 0, 0
        for row in self._board_status:
            y += 1
            for col in range(6):
                x += 1
                row.append(Dot(x, y))

    def is_hidden(self):
        return self._hid

    def get_dot(self, dot):
        """Возвращаем точку (Dot) с игровой доски по координатам входной точки (Dot)"""
        return self._board_status[dot.vals[1] - 1][dot.vals[0] - 1]

    def add_ship(self, length):
        print(f'Ставим корабль длины {length}')  # Собираем данные для создания корабля
        while True:  # Цикл для проверки ввода координат
            coords = input('Укажите координаты точки размещения через пробел: ').split()
            if coords[0].isdigit() and coords[1].isdigit():
                dot = Dot(*list(map(int, coords)))
                if Board.out(dot):  # Проверка диапазона
                    raise BoardOutException(dot)
                else:
                    head_dot = Dot(int(coords[0]), int(coords[1]))
                    break
            else:
                raise TypeError('Неправильно указаны координаты')
        direction = input('Корабль ставим вертикально? Y/N  ').lower()  # Проверяем направление
        direction = any([direction == x for x in ['y', 'да', '1', 'н']])
        ship = Ship(head_dot, length, direction)

        try:  # Пробуем разместить корабль по указанным координатам
            place_approved = True
            for cell in ship.dots():  # Проверка доступности точек корабля на доске
                if place_approved:
                    place_approved = self.get_dot(cell).is_free
            for cell in self.contour(ship):  # Проверка доступности точек вокруг корабля
                if place_approved:
                    place_approved = self.get_dot(cell).is_free
            if not place_approved:
                raise ShipPlacementError
        except ShipPlacementError:
            print('Атата однако')  # ПОПРАВИТЬ !!!
        else:
            # Добавляем корабль на доску
            for cell in ship.dots():
                self.get_dot(cell).is_free = False
                self.get_dot(cell).char = '■'
            self._fleet_list.append(ship)
            self._ships_count += 1

    @staticmethod
    def contour(ship):
        """Возвращает список Dot объектов вокруг корабля (не с доски)"""
        contour_list = []
        for cell in ship.dots():  # Обходим все точки принадлежащие кораблю
            vals = cell.vals  # координаты текущей точки сокращенно
            for y in range(vals[1] - 1, vals[1] + 2):  # Обходим все соседние точки
                for x in range(vals[0] - 1, vals[0] + 2):
                    if Board.out(Dot(x, y)):
                        continue
                    if Dot(x, y) not in contour_list and Dot(x, y) not in ship.dots():
                        contour_list.append(Dot(x, y))  # Собираем точки без дублей и клеток корабля

        return contour_list

    def show_board(self):
        print('   1 2 3 4 5 6')
        i = 1
        for row in self._board_status:
            print(i, end=' ')
            i += 1
            for item in row:
                if item.char == '■' and self.is_hidden():
                    print(' O', end='')
                else:
                    print(f' {item.char}', end='')
            print()


    @staticmethod
    def out(dot):
        """Возвращает True если точка (Dot) за пределами поля"""
        return False if dot.vals[0] in range(1, 7) and dot.vals[1] in range(1, 7) else True

    def shot(self):
        pass

