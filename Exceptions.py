class BoardOutException(Exception):
    def __init__(self, dot, msg='находится вне игрового поля'):
        self.dot = dot
        self.msg = msg

    def __str__(self):
        return f'Точка ({self.dot}) -> {self.msg}'


class ShipDirectionError(Exception):    # МОЖНО УДАЛИТЬ, ПЕРЕДЕЛАТЬ direction НА boolean
    def __init__(self, direction, msg='направление указано неверно'):
        self.direction = direction
        self.msg = msg

    def __str__(self):
        return f'{self.direction} - {self.msg}'


class ShipPlacementError(Exception):
    def __init__(self, msg='невозможно поставить'):
        self.msg = msg
