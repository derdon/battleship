from random import randrange, choice as random_choice

from battleship import logger
from battleship.field import GameField, Cell
from battleship.ships import Ship
from battleship.validators import validate_ship_coordinates
from battleship.exceptions import OutOfFieldError
from battleship.utils import Coordinates

DEFAULT_FIELD_WIDTH = 10
DEFAULT_FIELD_HEIGHT = 10

DEFAULT_MIN_SHIP_LENGTH = 2
DEFAULT_MAX_SHIP_LENGTH = 5


class Player(object):
    def __init__(self, opponents_field=None, field_width=DEFAULT_FIELD_WIDTH,
                 field_height=DEFAULT_FIELD_HEIGHT):
        self.own_field = GameField(field_width, field_height)
        if opponents_field is None:
            self.opponents_field = GameField(field_width, field_height)
        else:
            self.opponents_field = opponents_field
        self.own_ships = set()
        self._number_of_picks = 0

    def add_ship_randomly(self, length=None):
        '''
        length: the length of the ship which will be added; if not given, a
        random value in the intervall [2; 5] is used
        '''
        logger.debug('calling Player.add_ship_randomly')
        start_x = randrange(DEFAULT_FIELD_WIDTH)
        start_y = randrange(DEFAULT_FIELD_HEIGHT)
        start_coordinates = Coordinates(start_x, start_y)
        if length is None:
            length = randrange(
                DEFAULT_MIN_SHIP_LENGTH, DEFAULT_MAX_SHIP_LENGTH + 1)
        is_horintal = random_choice((True, False))
        if is_horintal:
            new_x_coordinate = start_coordinates.x + length
            end_coordinates = Coordinates(
                new_x_coordinate,
                start_coordinates.y)
        else:
            new_y_coordinates = start_coordinates.y + length
            end_coordinates = Coordinates(
                start_coordinates.x,
                new_y_coordinates)
        try:
            validate_ship_coordinates(
                self.own_field, self.own_ships,
                start_coordinates, end_coordinates)
        except OutOfFieldError:
            logger.debug('out of field')
            # `length` was *added* which caused the ship to overlap a border of
            # the field
            # ->
            # `length` must be *subtracted* from the corresponding
            # coordinate of the start point
            if is_horintal:
                end_coordinates_x = start_coordinates.x - length
                end_coordinates = Coordinates(
                    end_coordinates_x,
                    end_coordinates.y)
            else:
                end_coordinates_y = start_coordinates.y - length
                end_coordinates = Coordinates(
                    end_coordinates.x,
                    end_coordinates_y)
        logger.debug(repr((start_coordinates, end_coordinates)))
        self.add_ship(start_coordinates, end_coordinates)

    def add_ship(self, start_coordinates, end_coordinates):
        validate_ship_coordinates(
            self.own_field, self.own_ships, start_coordinates, end_coordinates)
        ship = Ship(start_coordinates, end_coordinates)
        for coordinates in ship.get_all_coordinates():
            self.own_field[coordinates] = Cell(True, coordinates)
        # FIXME: is this really necessary?!
        self.own_ships.add(ship)

    def pick_cell(self, coordinates):
        self._number_of_picks += 1
        return self.opponents_field[coordinates]

    def surrender(self):
        raise NotImplementedError()
