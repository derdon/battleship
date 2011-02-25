from battleship.field import GameField
from battleship.ships import Ship
from battleship.utils import Coordinates


def pytest_funcarg__horizontal_ship(request):
    return Ship(Coordinates(2, 5), Coordinates(4, 5))


def pytest_funcarg__vertical_ship(request):
    return Ship(Coordinates(3, 4), Coordinates(3, 6))


def pytest_funcarg__nonstraight_ship(request):
    return Ship(Coordinates(1, 7), Coordinates(2, 8))


def pytest_funcarg__game_field(request):
    return GameField(3, 4)


def pytest_funcarg__own_field(request):
    return GameField(10, 10)


def pytest_funcarg__own_ships(request):
    return [Ship(Coordinates(0, 0), Coordinates(3, 4))]
