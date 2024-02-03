# Внешняя логика игры — пользовательский интерфейс,
# искусственный интеллект, игровой контроллер,
# который считает побитые корабли.

import random
from InnerLogic import *


class Player:
    _my_board = None
    _enemy_board = None

    def __init__(self, my_board, enemy_board):
        self._my_board = my_board
        self._enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            dot = self.ask()
            try:
                if self._enemy_board.shot(dot):
                    break
            except TypeError:
                print('Что то пошло не так в данных выстрела')
        return True


class AI(Player):
    def ask(self):
        x = random.randrange(1, 7)
        y = random.randrange(1, 7)
        return Dot(x, y)


class User(Player):
    def ask(self):
        print('Координаты указываем через пробел.')
        coords = None
        while True:  # Цикл для проверки ввода координат
            coords = input('Куда стреляем? ').split()
            try:
                if coords[0].isdigit() and coords[1].isdigit():
                    dot = Dot(*list(map(int, coords)))
                    if Board.out(dot):  # Проверка диапазона
                        raise BoardOutException(dot)
                    else:
                        return dot
                else:
                    raise TypeError()
            except IndexError:
                print('Неправильно указаны координаты')
                continue
            except TypeError:
                print('Неправильно указаны координаты')
                continue
            except BoardOutException:
                continue


class Game:
    _ship_size_list = [3, 2, 2, 1, 1, 1, 1]

    def __init__(self, user, user_board, ai, ai_board):
        self.user = user
        self.user_board = user_board
        self.ai = ai
        self.ai_board = ai_board

    def random_board(self):
        pass

    @staticmethod
    def greet():
        print("""Привет! Это игра Морской бой.
        Как играть:
        Есть 2 игровых доски. Одна представляют вашу, где стоят ваши корабли.
        Другая же - доска противника, по которой будем стрелять.
        Размер игровой доски 6х6 поэтому координаты точки указываем через пробел в пределах от 1 до 6.
        Корабли ставятся вертикально(вниз) или горизонтально(вправо) от указанной точки.
        Всего у каждого игрока кораблей будет 7. Один трехпалубный, 2 двухпалубных и 4 однопалубных.
        Победит тот кто подобъет все первым.
        Если игрок попадает по кораблю противника, он получает дополнительных ход.""")

    def loop(self):
        pass

    def start(self):
        self.greet()
        self.loop()

# coords = None
# dot = None
# print('Координаты указываем через пробел.')
# while True:  # Цикл для проверки ввода координат
#     if not self.is_hidden():
#         coords = input('Куда стреляем? ').split()
#     try:
#         if coords:
#             if coords[0].isdigit() and coords[1].isdigit():
#                 dot = Dot(*list(map(int, coords)))
#                 if Board.out(dot):  # Проверка диапазона
#                     raise BoardOutException(dot)
#             else:
#                 raise TypeError()
#         else:
#             x = random.randrange(1, 7)
#             y = random.randrange(1, 7)
#             dot = Dot(x, y)
#     except IndexError:
#         print('Неправильно указаны координаты')
#         continue
#     except TypeError:
#         print('Неправильно указаны координаты')
#         continue
#     except BoardOutException:
#         continue
