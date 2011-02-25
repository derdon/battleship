class Error(Exception):
    'Base exception class for all custom defined exceptions'


class ShipNotStraightError(Error):
    pass


class ShipTooSmallError(Error):
    def __init__(self, min_length):
        self.min_length = min_length

    def __str__(self):
        return 'the ship must have a length of %d or greater' % (self.min_length, )


class OutOfFieldError(Error):
    def __init__(self, field, ship):
        self.field = field
        self.ship = ship

    def __str__(self):
        return 'the ship %r crosses one of the borders of the field %r' % (
            self.ship, self.field)


class ShipAlreadyAdded(Error):
    def __init__(self, ship):
        self.ship = ship

    def __str__(self):
        return 'the ship %r has already been added to the field' % (self.ship, )
