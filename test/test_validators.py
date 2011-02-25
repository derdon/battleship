from __future__ import with_statement

from functools import partial

import pytest

from battleship.exceptions import OutOfFieldError, ShipAlreadyAdded, \
    ShipNotStraightError, ShipTooSmallError
from battleship.validators import validate_ship_coordinates
from battleship.utils import Coordinates


class TestValidateShipCoordinates(object):
    def test_already_added(self, own_field, own_ships):
        with pytest.raises(ShipAlreadyAdded):
            validate_ship_coordinates(
                own_field, own_ships, Coordinates(0, 0), Coordinates(3, 4))

    def test_nonstraight(self, own_field, own_ships, nonstraight_ship):
        start = nonstraight_ship.start_coordinates
        end = nonstraight_ship.end_coordinates
        with pytest.raises(ShipNotStraightError):
            validate_ship_coordinates(own_field, own_ships, start, end)

    def test_length_too_low(self, own_field, own_ships):
        co = Coordinates(4, 7)
        with pytest.raises(ShipTooSmallError):
            validate_ship_coordinates(own_field, own_ships, co, co)

    def test_out_of_field(self, own_field, own_ships):
        validate = partial(validate_ship_coordinates, own_field, own_ships)
        with pytest.raises(OutOfFieldError):
            validate(Coordinates(10, 5), Coordinates(15, 5))
        with pytest.raises(OutOfFieldError):
            validate(Coordinates(5, 8), Coordinates(5, 13))
