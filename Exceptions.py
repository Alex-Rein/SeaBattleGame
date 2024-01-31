class BoardOutException(Exception):
    def __init__(self, dot, msg='находится вне игрового поля'):
        self.dot = dot
        self.msg = msg

    def __str__(self):
        return f'Точка ({self.dot}) -> {self.msg}'


class ShipPlacementError(Exception):
    def __init__(self, msg='невозможно поставить'):
        self.msg = msg
