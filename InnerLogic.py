# Внутренняя логика игры — корабли,
# игровая доска и вся логика связанная с ней. ■

# direction для корабля проверяется упрощенно как значение bool. Чтобы не заморачиваться
from Exceptions import *


class Dot:
    def __init__(self, x, y):
        self._is_free = True
        self._char = 'O'
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other.vals[0] and self._y == other.vals[1]

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

    @property
    def life(self):
        return self._life

    @life.setter
    def life(self, value):
        if type(value) is int:
            self._life = value

    def dots(self):
        """Возвращает список всех точек (Dot) корабля"""
        dot_list = [self._head_dot]
        for i in range(1, self._length):
            if self._direction:
                dot_list.append(Dot(self._head_dot.vals[0], self._head_dot.vals[1] + i))
            else:
                dot_list.append(Dot(self._head_dot.vals[0] + i, self._head_dot.vals[1]))
        return dot_list


class Board:
    def __init__(self, hidden=False):
        """Для компьютерного игрока нужно передать bool значение True"""
        self._board_status = [[], [], [], [], [], []]
        self.fleet_list = []
        self._ships_count = 0
        self._hid = hidden
        x, y = 0, 0
        for row in self._board_status:
            y += 1
            for col in range(6):
                x += 1
                row.append(Dot(x, y))

    @property
    def ships_count(self):
        return self._ships_count

    @ships_count.setter
    def ships_count(self, value):
        if type(value) is int:
            self._ships_count = value

    def is_hidden(self):
        return self._hid

    def get_dot(self, dot):
        """Возвращаем точку (Dot) с игровой доски по координатам входной точки (Dot)"""
        return self._board_status[dot.vals[1] - 1][dot.vals[0] - 1]

    def add_ship(self, head_dot, length, direction):
        """Добавляем корабль на доску с заранее заданными параметрами. Возвращает True при успешной установке."""
        while True:
            success = False
            try:  # Пробуем разместить корабль по указанным координатам
                ship = Ship(head_dot=head_dot, length=length, direction=direction)
                place_approved = True
                for cell in ship.dots():  # Проверка доступности точек корабля на доске
                    if self.out(cell):
                        raise BoardOutException()
                    if place_approved:
                        place_approved = self.get_dot(cell).is_free
                for cell in self.contour(ship):  # Проверка доступности точек вокруг корабля
                    if self.out(cell):
                        raise BoardOutException()
                    if place_approved:
                        place_approved = self.get_dot(cell).is_free
                if not place_approved:
                    raise ShipPlacementError()
            except BoardOutException as e:
                # print(e)
                continue
            except ShipPlacementError as e:
                # print(e)
                continue
            except TypeError as e:
                print('Введены неправильные параметры корабля')
            else:
                # Добавляем корабль на доску
                for cell in ship.dots():
                    self.get_dot(cell).is_free = False
                    self.get_dot(cell).char = '■'
                self.fleet_list.append(ship)
                self.ships_count += 1
                success = True
            finally:
                return success

    def add_ship_manual(self, length):
        """Добавляем корабль на доску вручную задавая параметры корабля.
        ОСТОРОЖНО! Ситуация когда корабль невозможно поставить не обработана."""
        while True:  # Цикл для проверки ввода координат
            print(f'Ставим корабль длины {length}')  # Собираем данные для создания корабля
            coords = input('Укажите координаты точки размещения через пробел: ').split()
            head_dot = None
            try:
                if coords[0].isdigit() and coords[1].isdigit():
                    head_dot = Dot(*list(map(int, coords)))
                    if Board.out(head_dot):  # Проверка диапазона
                        raise BoardOutException()
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

        if length == 1:  # Проверяем направление упрощенно :)
            direction = True
        else:
            direction = input('Корабль ставим вертикально? Y/N  ').lower()
            direction = any([direction == x for x in ['y', 'да', '1', 'н']])

        ship = Ship(head_dot, length, direction)
        success = False

        try:  # Пробуем разместить корабль по указанным координатам
            place_approved = True
            for cell in ship.dots():  # Проверка доступности точек корабля на доске
                if self.out(cell):
                    raise BoardOutException()
                if place_approved:
                    place_approved = self.get_dot(cell).is_free
            for cell in self.contour(ship):  # Проверка доступности точек вокруг корабля
                if self.out(cell):
                    raise BoardOutException()
                if place_approved:
                    place_approved = self.get_dot(cell).is_free
            if not place_approved:
                raise ShipPlacementError
        except BoardOutException as e:
            print('Размещение вышло за границы доски')
            print(e)
        except ShipPlacementError:
            print('Тут нельзя поставить. Что то уже стоит рядом.')
        else:
            # Добавляем корабль на доску
            for cell in ship.dots():
                self.get_dot(cell).is_free = False
                self.get_dot(cell).char = '■'
            self.fleet_list.append(ship)
            self.ships_count += 1
            success = True
        finally:
            return success

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

    def show(self):
        """Показывает доску в зависимости от параметра hidden"""
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
        print()

    @staticmethod
    def out(dot):
        """Возвращает True если точка (Dot) за пределами поля"""
        return False if dot.vals[0] in range(1, 7) and dot.vals[1] in range(1, 7) else True

    def shot(self, dot):
        if Board.out(dot):  # Проверка диапазона
            raise BoardOutException()

        char = self.get_dot(dot).char  # Проверка символа куда стреляем
        if char == 'O':
            self.get_dot(dot).char = 'T'
        elif char == '■':
            self.get_dot(dot).char = 'X'
            return True
        else:  # Подразумевается что это char == 'T' or char == 'X'
            raise DotIsShottedError()

    def get_ship(self, dot):
        for ship in self.fleet_list:
            for cell in ship.dots():
                if cell == dot:
                    return ship

    @staticmethod
    def damage_ship(ship):
        ship.life -= 1
        if ship.life == 0:
            return True
