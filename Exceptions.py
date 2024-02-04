class BoardOutException(Exception):
    def __init__(self, msg='Точка находится вне игрового поля'):
        self.msg = msg

    def __str__(self):
        return self.msg


class ShipPlacementError(Exception):
    def __init__(self, msg='Невозможно поставить корабль'):
        self.msg = msg

    def __str__(self):
        return self.msg


class DotIsShottedError(Exception):
    def __init__(self,  msg='В эту точку уже стреляли'):
        self.msg = msg

    def __str__(self):
        return self.msg
