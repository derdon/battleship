from itertools import imap

from battleship.utils import Coordinates


class GameField(object):
    def __init__(self, cols, rows, cell_kwargs=None):
        '''
        - cols: the number of columns for the field
        - rows: the number of rows for the field
        - cell_kwargs: a mapping which defines one or more parameters of
          ``unknown``, ``water``, ``ship``. See the class ``Cell`` for details.
        '''
        if cell_kwargs is None:
            cell_kwargs = {}
        self.field = [
            [Cell(None, Coordinates(x, y), **cell_kwargs) for x in xrange(cols)]
                for y in xrange(rows)]

    @property
    def rows(self):
        return len(self.field)

    @property
    def cols(self):
        return max(imap(len, self.field))

    # append_row = self.field.append
    def append_row(self, row):
        self.field.append(row)

    def append_rows(self, rows):
        for row in rows:
            self.append_row(row)

    def append_column(self, col):
        raise NotImplementedError

    def append_columns(self, cols):
        for col in cols:
            self.append_column(col)

    def prepend_row(self, row):
        self.insert_row(0, row)

    def prepend_column(self, col):
        self.insert_column(0, col)

    # insert_row = self.field.insert
    def insert_row(self, index, row):
        self.field.insert(index, row)

    def insert_column(self, index, col):
        raise NotImplementedError

    def remove_row(self, row):
        raise NotImplementedError

    def remove_column(self, col):
        raise NotImplementedError

    def __repr__(self):
        return '%s(columns=%d, rows=%d)' % (
            self.__class__.__name__,
            self.cols,
            self.rows)

    def __getitem__(self, (column, row)):
        if row is Ellipsis and column is Ellipsis:
            return self.__class__(self.cols, self.rows)
        if column is Ellipsis:
            if isinstance(row, slice):
                return map(list, zip(*self.field)[row])
            else:
                return list(zip(*self.field)[row])
        if row is Ellipsis:
            return self.field[column]
        return self.field[row][column]

    def __setitem__(self, (column, row), value):
        self.field[row][column] = value

    def __delitem__(self, (column, row)):
        if row is Ellipsis and column is Ellipsis:
            self.field = []
        elif column is Ellipsis:
            for i, x in enumerate(self.field[:]):
                del self.field[i][row]
        elif row is Ellipsis:
            del self.field[column]
        else:
            raise TypeError(
                'it is not possible to delete single cells. Remove whole rows '
                'or columns by using the ellipsis parameter for either of '
                'them.')

    def __iter__(self):
        return iter(self.field)

    def __contains__(self, cell):
        for row in self.field:
            for col in row:
                if col == cell:
                    return True
        return False

    def __nonzero__(self):
        return any(self.field)

    def __eq__(self, other):
        return self.field == other.field

    def __ne__(self, other):
        return not (self == other)

    __hash__ = None


class Cell(object):
    # TODO: say in the docstring that the attributes shouldn't be overwritten,
    # once an instance is created
    def __init__(self, val, coordinates, unknown=' ', water='~', ship='X'):
        '''create a new Cell object with the value `val` and the given
        coordinates. `val` must be one of `True`, `False`, `None`
        '''
        if val not in set([True, False, None]):
            raise TypeError(
                'expected True, False or None. Got %r instead' % (type(val), ))
        self.val = val
        self.coordinates = coordinates
        self.unknown = unknown
        self.water = water
        self.ship = ship

    def __repr__(self):
        return '%s(value=%r, %r)' % (
            self.__class__.__name__,
            self.val,
            self.coordinates)

    def __str__(self):
        if self.val is None:
            return self.unknown
        elif self.val:
            return self.ship
        elif not self.val:
            return self.water

    def __hash__(self):
        return hash((
            self.val,
            self.coordinates,
            self.unknown,
            self.water,
            self.ship
        ))

    def __eq__(self, other):
        return all((
            self.val == other.val,
            self.coordinates == other.coordinates,
            self.unknown == other.unknown,
            self.water == other.water,
            self.ship == other.ship
        ))

    def __ne__(self, other):
        return not (self == other)
