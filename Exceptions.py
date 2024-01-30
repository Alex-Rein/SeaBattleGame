class BoardOutException(Exception):
    def __init__(self, dot, msg='находится вне игрового поля'):
        self.dot = dot
        self.msg = msg

    def __str__(self):
        return f'Точка ({self.dot}) -> {self.msg}'


class ShipDirectionError(Exception):
    def __init__(self, direction, msg='направление указано не верно'):
        self.direction = direction
        self.msg = msg

    def __str__(self):
        return f'{self.direction} - {self.msg}'
