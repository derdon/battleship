from functools import partial

from battleship.ships import Ship
from battleship.exceptions import OutOfFieldError, ShipAlreadyAdded, \
    ShipNotStraightError, ShipTooSmallError


def validate_ship_coordinates(field, own_ships, start, end):
    ship = Ship(start, end)
    if ship in own_ships:
        raise ShipAlreadyAdded(ship)
    if not (ship.is_horizontal or ship.is_vertical):
        raise ShipNotStraightError()
    # make sure that the ship's length is greater than 1
    if start == end:
        raise ShipTooSmallError(2)
    # make sure that the ship does not cross the borders of the
    # field
    is_in_field = partial(coordinates_in_field, field)
    if not (is_in_field(start) and is_in_field(end)):
        raise OutOfFieldError(field, ship)


def coordinates_in_field(field, coordinates):
    return coordinates.x < field.cols and coordinates.y < field.rows
