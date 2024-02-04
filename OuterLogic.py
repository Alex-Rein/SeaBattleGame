# Внешняя логика игры — пользовательский интерфейс,
# искусственный интеллект, игровой контроллер,
# который считает побитые корабли.

import random
from InnerLogic import *


class Player:
    def __init__(self, this_board, enemy_board):
        self.this_board = this_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self, mode=True):
        """Передать параметр bool = False для отключение сообщений об ошибках выстрелов для компьютера"""
        add_move = False
        while True:
            dot = self.ask()
            try:
                if self.enemy_board.shot(dot):
                    print('Попал! Стреляем еще раз.')
                    ship = self.enemy_board.get_ship(dot)
                    if self.enemy_board.damage_ship(ship):
                        print('Корабль противника уничтожен!')
                        for dot in self.enemy_board.contour(ship):
                            self.enemy_board.get_dot(dot).char = 'T'
                        self.enemy_board.ships_count -= 1
                        self.enemy_board.fleet_list.remove(ship)
                    add_move = True
            except TypeError:
                print('Что то пошло не так в данных выстрела')
                continue
            except BoardOutException as e:
                if mode:
                    print(e)
                continue
            except DotIsShottedError as e:
                if mode:
                    print(e)
                continue
            else:
                break
        return add_move


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
                        raise BoardOutException()
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

    def __init__(self):
        self.user_board = Board()
        self.ai_board = Board(True)
        # self.ai_board = Board()  # ДЛЯ ДЕБАГГА, ПОСЛЕ ПРОВЕРКИ ЗАКОММЕНТИТЬ И РАСКОММЕНТИТЬ СТРОКУ ВЫШЕ
        self.user = User(self.user_board, self.ai_board)
        self.ai = AI(self.ai_board, self.user_board)

    def random_board(self, board, user=True):
        """Передать параметр bool = False если передается доска АИ"""
        mode = False  # Переменная для выбора как ставим корабли
        new_gen = False
        while True:  # Цикл полной генерации игровой доски
            if new_gen:
                board = Board() if user else Board(True)  # Новая доска для игрока
            new_gen = False  # Триггер для выхода из генерации новой доски

            if user:
                mode = input('Будем ставить корабли вручную? Y/N ').lower()
                mode = any([mode == x for x in ['y', 'да', '1', 'н']])

            for size in self._ship_size_list:  # Пробуем ставить корабли каждого типоразмера
                i = 0
                ship_placed = False
                while not ship_placed:
                    i += 1
                    if i > 5000:
                        new_gen = True
                        break

                    if mode and i > 3:  # Если ставим корабли вручную
                        print('Превышено количество попыток для установки, давай заново)')
                        new_gen = True
                        break
                    elif mode:
                        board.show()
                        if board.add_ship_manual(size):
                            ship_placed = True
                            break
                        else:
                            continue
                    else:  # Ставим рандомно
                        x = random.randrange(1, 7)  # Генерируем точку куда ставим
                        y = random.randrange(1, 7)
                        dot = Dot(x, y)

                        rnd = random.randrange(100)  # Случайно выбираем направление
                        direction = True if rnd in range(50) else False

                        if board.add_ship(head_dot=dot, length=size, direction=direction):
                            ship_placed = True
                            break
            if not new_gen:  # Проверка на выход из генерации новой доски
                break
            break

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
        Если игрок попадает по кораблю противника, он получает дополнительных ход.
        """)

    def loop(self):
        print('Доска игрока')
        self.user_board.show()
        not_win = True
        while not_win:
            while self.ai_board.ships_count:
                print()
                print('Доска противника')
                self.ai_board.show()
                print('Ходит Игрок!')
                if not self.user.move():
                    break
            if self.win_check(self.user):
                print('Доска противника')
                self.ai_board.show()
                Game.winner('Игрок')
                not_win = False
                break

            print('Ходит Компудахтер!')
            while self.user_board.ships_count:
                if not self.ai.move(False):
                    break
            if self.win_check(self.ai):

                Game.winner('Компудахтер')
                not_win = False
                break
            else:
                print('Доска игрока')
                self.user_board.show()

    def start(self):
        self.greet()
        self.random_board(self.user_board)
        self.random_board(self.ai_board, False)
        self.loop()

    def start_debug(self):
        self.greet()
        self.user_board.add_ship(Dot(1, 1), 3, True)
        self.ai_board.add_ship(Dot(6, 1), 2, True)
        self.loop()

    @staticmethod
    def win_check(player):
        if player.enemy_board.ships_count == 0:
            return True

    @staticmethod
    def winner(player):
        print()
        print('Па-ба-ба-бам! Вражеский флот разбит!')
        print(f'Великий генерал {player} победил!')
