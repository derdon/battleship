from itertools import izip, repeat

from battleship.exceptions import ShipNotStraightError
from battleship.utils import Coordinates


class Ship(object):
    def __init__(self, start_coordinates, end_coordinates):
        self.start_coordinates = start_coordinates
        self.end_coordinates = end_coordinates

    def __repr__(self):
        return '%s(%r, %r)' % (
            self.__class__.__name__,
            self.start_coordinates,
            self.end_coordinates)

    @property
    def is_horizontal(self):
        return self.start_coordinates.y == self.end_coordinates.y

    @property
    def is_vertical(self):
        return self.start_coordinates.x == self.end_coordinates.x

    def get_all_coordinates(self):
        start = self.start_coordinates
        end = self.end_coordinates
        if self.is_horizontal:
            for x, y in izip(xrange(start.x, end.x + 1), repeat(start.y)):
                yield Coordinates(x, y)
        elif self.is_vertical:
            for x, y in izip(repeat(start.x), xrange(start.y, end.y + 1)):
                yield Coordinates(x, y)
        else:
            raise ShipNotStraightError()

    def __eq__(self, other):
        # the alignment of a ship does not matter: two ships are equal if the
        # two cells by which they are defined are equal; the order of these
        # cells is not important
        self_coordinates = set([self.start_coordinates, self.end_coordinates])
        other_coordinates = set(
            [other.start_coordinates, other.end_coordinates])
        return self_coordinates == other_coordinates

    def __ne__(self, other):
        return not (self == other)

    def __contains__(self, coordinates):
        return coordinates in self.get_all_coordinates()

    def intersects(self, other_ship):
        own_coordinates = set(self.get_all_coordinates())
        other_coordinates = set(other_ship.get_all_coordinates())
        return bool(own_coordinates & other_coordinates)
