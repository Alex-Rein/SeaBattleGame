# Внутренняя логика игры — корабли,
# игровая доска и вся логика связанная с ней. ■
import random

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
        while True:  # Общий цикл для установки корабля
            while True:  # Цикл для проверки ввода координат
                print(f'Ставим корабль длины {length}')  # Собираем данные для создания корабля
                coords = input('Укажите координаты точки размещения через пробел: ').split()
                head_dot = None
                try:
                    if coords[0].isdigit() and coords[1].isdigit():
                        head_dot = Dot(*list(map(int, coords)))
                        if Board.out(head_dot):  # Проверка диапазона
                            raise BoardOutException(head_dot)
                        else:
                            break
                    else:
                        raise TypeError
                except IndexError:
                    print('Неправильно указаны координаты')
                    continue
                except TypeError:
                    print('Неправильно указаны координаты')
                    continue
                except BoardOutException as e:
                    print(e)
                    continue

            direction = input('Корабль ставим вертикально? Y/N  ').lower()  # Проверяем направление упрощенно :)
            direction = any([direction == x for x in ['y', 'да', '1', 'н']])
            ship = Ship(head_dot, length, direction)

            try:  # Пробуем разместить корабль по указанным координатам
                place_approved = True
                for cell in ship.dots():  # Проверка доступности точек корабля на доске
                    if self.out(cell):
                        raise BoardOutException(cell)
                    if place_approved:
                        place_approved = self.get_dot(cell).is_free
                for cell in self.contour(ship):  # Проверка доступности точек вокруг корабля
                    if self.out(cell):
                        raise BoardOutException(cell)
                    if place_approved:
                        place_approved = self.get_dot(cell).is_free
                if not place_approved:
                    raise ShipPlacementError
            except BoardOutException as e:
                print('Размещение вышло за границы доски')
                print(e)
                continue
            except ShipPlacementError:
                print('Тут нельзя поставить. Что то уже стоит рядом.')
                continue
            else:
                # Добавляем корабль на доску
                for cell in ship.dots():
                    self.get_dot(cell).is_free = False
                    self.get_dot(cell).char = '■'
                self._fleet_list.append(ship)
                self._ships_count += 1
                break

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
        coords = None
        dot = None
        print('Координаты указываем через пробел.')
        while True:  # Цикл для проверки ввода координат
            if not self.is_hidden():
                coords = input('Куда стреляем? ').split()
            try:
                if coords:
                    if coords[0].isdigit() and coords[1].isdigit():
                        dot = Dot(*list(map(int, coords)))
                        if Board.out(dot):  # Проверка диапазона
                            raise BoardOutException(dot)
                    else:
                        raise TypeError()
                else:
                    x = random.randrange(1, 7)
                    y = random.randrange(1, 7)
                    dot = Dot(x, y)
            except IndexError:
                print('Неправильно указаны координаты')
                continue
            except TypeError:
                print('Неправильно указаны координаты')
                continue
            except BoardOutException:
                continue

            char = self.get_dot(dot).char
            try:
                if char == 'O':
                    self.get_dot(dot).char = 'T'
                    break
                elif char == '■':
                    self.get_dot(dot).char = 'X'
                    if not self.is_hidden():
                        print('Йо-хо-хо, мы в кого то попали! Заряжай еще раз!')
                else:  # Подразумевается что это char == 'T' or char == 'X'
                    raise DotIsShottedError(dot)
            except DotIsShottedError:
                if not self.is_hidden():
                    print('Оказалось что сюда уже стреляли! Надо бы стрельнуть куда то еще!')
                    continue
