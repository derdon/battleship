from __future__ import with_statement

import pytest

from battleship.ships import Ship
from battleship.exceptions import ShipNotStraightError
from battleship.utils import Coordinates


class TestShipAlignment(object):
    def test_is_horizontal(self, horizontal_ship, vertical_ship):
        assert horizontal_ship.is_horizontal
        assert not vertical_ship.is_horizontal

    def test_is_vertical(self, horizontal_ship, vertical_ship):
        assert not horizontal_ship.is_vertical
        assert vertical_ship.is_vertical

    def test_is_neither_horizontal_nor_vertical(self, nonstraight_ship):
        assert not nonstraight_ship.is_horizontal
        assert not nonstraight_ship.is_vertical


class TestShipAllCoordinates(object):
    def test_horizontal(self, horizontal_ship):
        all_coordinates = list(horizontal_ship.get_all_coordinates())
        assert all_coordinates == [
            Coordinates(2, 5), Coordinates(3, 5), Coordinates(4, 5)]

    def test_vertical(self, vertical_ship):
        all_coordinates = list(vertical_ship.get_all_coordinates())
        assert all_coordinates == [
            Coordinates(3, 4), Coordinates(3, 5), Coordinates(3, 6)]

    def test_nonstraight(self, nonstraight_ship):
        with pytest.raises(ShipNotStraightError):
            list(nonstraight_ship.get_all_coordinates())


class TestShipIntersect(object):
    def test_intersect(self, horizontal_ship, vertical_ship):
        assert horizontal_ship.intersects(vertical_ship)
        assert vertical_ship.intersects(horizontal_ship)

    def test_fails(self, horizontal_ship, vertical_ship, nonstraight_ship):
        funcs = [horizontal_ship.intersects, vertical_ship.intersects]
        for func in funcs:
            with pytest.raises(ShipNotStraightError):
                func(nonstraight_ship)


class TestShipEquality(object):
    def test_identical(self):
        ship1 = Ship(Coordinates(1, 2), Coordinates(3, 4))
        ship2 = Ship(Coordinates(1, 2), Coordinates(3, 4))
        assert ship1 == ship2

    def test_reversed_start_and_end(self):
        ship1 = Ship(Coordinates(1, 2), Coordinates(3, 4))
        ship2 = Ship(Coordinates(3, 4), Coordinates(1, 2))
        assert ship1 == ship2


def test_contains(horizontal_ship):
    assert Coordinates(3, 5) in horizontal_ship
