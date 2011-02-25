from __future__ import with_statement, division

import pytest

from battleship.field import GameField, Cell
from battleship.utils import Coordinates


class TestGameField(object):
    def test_init(self, game_field):
        assert game_field.field == [
            [
                Cell(None, Coordinates(0, 0)),
                Cell(None, Coordinates(1, 0)),
                Cell(None, Coordinates(2, 0)),
            ],
            [
                Cell(None, Coordinates(0, 1)),
                Cell(None, Coordinates(1, 1)),
                Cell(None, Coordinates(2, 1)),
            ],
            [
                Cell(None, Coordinates(0, 2)),
                Cell(None, Coordinates(1, 2)),
                Cell(None, Coordinates(2, 2)),
            ],
            [
                Cell(None, Coordinates(0, 3)),
                Cell(None, Coordinates(1, 3)),
                Cell(None, Coordinates(2, 3)),
            ]
        ]

    def test_rows_property(self, game_field):
        assert game_field.rows == 4

    def test_cols_property(self, game_field):
        assert game_field.cols == 3

    def test_setitem(self, game_field):
        coordinates = Coordinates(1, 1)
        game_field[coordinates] = Cell(True, coordinates)
        assert game_field[coordinates] == Cell(True, coordinates)

    def test_contains(self, game_field):
        assert Cell(None, Coordinates(1, 2)) in game_field
        assert Cell(None, (1, 2)) in game_field

    def test_hashable(self, game_field):
        with pytest.raises(TypeError):
            hash(game_field)


class TestGameFieldGetitem(object):
    def test_non_accessible_cell(self, game_field):
        with pytest.raises(IndexError):
            game_field[3, 2]

    def test_accessible_cell(self, game_field):
        assert game_field[0, 1] == Cell(None, Coordinates(0, 1))

    def test_row_ellipsis(self, game_field):
        assert game_field[1, ...] == [
            Cell(None, Coordinates(0, 1)),
            Cell(None, Coordinates(1, 1)),
            Cell(None, Coordinates(2, 1))]

    def test_column_ellipsis(self, game_field):
        assert game_field[..., 1] == [
            Cell(None, Coordinates(1, 0)),
            Cell(None, Coordinates(1, 1)),
            Cell(None, Coordinates(1, 2)),
            Cell(None, Coordinates(1, 3))]

    def test_copy_field(self, game_field):
        copy_of_field = game_field[..., ...]
        assert game_field == copy_of_field

    def test_all_rows(self, game_field):
        all_rows = game_field[:, ...]
        assert len(all_rows) == 4
        assert all_rows == game_field.field

    def test_all_columns(self, game_field):
        all_cols = game_field[..., :]
        assert len(all_cols) == 3
        assert all_cols == [
            [
                Cell(None, Coordinates(0, 0)),
                Cell(None, Coordinates(0, 1)),
                Cell(None, Coordinates(0, 2)),
                Cell(None, Coordinates(0, 3))
            ],
            [
                Cell(None, Coordinates(1, 0)),
                Cell(None, Coordinates(1, 1)),
                Cell(None, Coordinates(1, 2)),
                Cell(None, Coordinates(1, 3))
            ],
            [
                Cell(None, Coordinates(2, 0)),
                Cell(None, Coordinates(2, 1)),
                Cell(None, Coordinates(2, 2)),
                Cell(None, Coordinates(2, 3)),
            ]
        ]

    def test_rows_sliced(self, game_field):
        selected_rows = game_field[::2, ...]
        assert len(selected_rows) == game_field.rows // 2 == 2
        assert selected_rows == [
            [
                Cell(None, Coordinates(0, 0)),
                Cell(None, Coordinates(1, 0)),
                Cell(None, Coordinates(2, 0)),
            ],
            [
                Cell(None, Coordinates(0, 2)),
                Cell(None, Coordinates(1, 2)),
                Cell(None, Coordinates(2, 2)),
            ]
        ]

    def test_columns_sliced(self, game_field):
        selected_cols = game_field[..., ::2]
        assert len(selected_cols) == 2
        assert selected_cols == [
            [
                Cell(None, Coordinates(0, 0)),
                Cell(None, Coordinates(0, 1)),
                Cell(None, Coordinates(0, 2)),
                Cell(None, Coordinates(0, 3))
            ],
            [
                Cell(None, Coordinates(2, 0)),
                Cell(None, Coordinates(2, 1)),
                Cell(None, Coordinates(2, 2)),
                Cell(None, Coordinates(2, 3)),
            ]
        ]


class TestGameFieldDelitem(object):
    def test_both_ints(self, game_field):
        with pytest.raises(TypeError):
            del game_field[2, 2]

    def test_both_ellipsis(self, game_field):
        del game_field[..., ...]
        assert game_field.field == []

    def test_row_ellipsis(self, game_field):
        # remove row #1
        del game_field[1, ...]
        assert game_field.rows == 3
        assert game_field.cols == 3
        assert game_field.field == [
            [
                Cell(None, Coordinates(0, 0)),
                Cell(None, Coordinates(1, 0)),
                Cell(None, Coordinates(2, 0)),
            ],
            [
                Cell(None, Coordinates(0, 2)),
                Cell(None, Coordinates(1, 2)),
                Cell(None, Coordinates(2, 2)),
            ],
            [
                Cell(None, Coordinates(0, 3)),
                Cell(None, Coordinates(1, 3)),
                Cell(None, Coordinates(2, 3)),
            ]
        ]

    def test_column_ellipsis(self, game_field):
        # remove column #2
        del game_field[..., 2]
        assert game_field.rows == 4
        assert game_field.cols == 2
        assert game_field.field == [
            [
                Cell(None, Coordinates(0, 0)),
                Cell(None, Coordinates(1, 0)),
            ],
            [
                Cell(None, Coordinates(0, 1)),
                Cell(None, Coordinates(1, 1)),
            ],
            [
                Cell(None, Coordinates(0, 2)),
                Cell(None, Coordinates(1, 2)),
            ],
            [
                Cell(None, Coordinates(0, 3)),
                Cell(None, Coordinates(1, 3)),
            ]
        ]

    def test_rows_sliced(self, game_field):
        # remove every second row, beginning with the first one,
        # i.e. the first and third row
        del game_field[::2, ...]
        assert game_field.rows == 2
        assert game_field.cols == 3
        assert game_field.field == [
            [
                Cell(None, Coordinates(0, 1)),
                Cell(None, Coordinates(1, 1)),
                Cell(None, Coordinates(2, 1)),
            ],
            [
                Cell(None, Coordinates(0, 3)),
                Cell(None, Coordinates(1, 3)),
                Cell(None, Coordinates(2, 3)),
            ]
        ]

    def test_columns_sliced(self, game_field):
        # remove every second column, beginning with the first one,
        # i.e. the first and third column
        del game_field[..., ::2]
        assert game_field.field == [
            [Cell(None, Coordinates(1, 0))],
            [Cell(None, Coordinates(1, 1))],
            [Cell(None, Coordinates(1, 2))],
            [Cell(None, Coordinates(1, 3))]
        ]


class TestGameFieldEquality(object):
    def test_equal(self):
        field1 = GameField(23, 42)
        field2 = GameField(23, 42)
        assert field1 == field2

    def test_equal_size_but_different_cell(self):
        field1 = GameField(23, 42)
        field2 = GameField(23, 42)
        field1[1, 1] = Cell(False, (1, 1))
        assert field1 != field2


class TestCellInit(object):
    def test_invalid_value(self):
        with pytest.raises(TypeError):
            Cell(42, Coordinates(0, 0))

    def test_custom_format(self):
        cell = Cell(True, Coordinates(2, 3), '?', '-', '#')
        assert cell.val
        assert cell.coordinates == Coordinates(2, 3)
        assert cell.unknown == '?'
        assert cell.water == '-'
        assert cell.ship == '#'


class TestCellEquality(object):
    def test_equal(self):
        cell1 = Cell(True, Coordinates(23, 42))
        cell2 = Cell(True, Coordinates(23, 42))
        assert cell1 == cell2

    def test_coordinates_and_tuple(self):
        cell1 = Cell(True, Coordinates(23, 42))
        cell2 = Cell(True, (23, 42))
        assert cell1 == cell2

    def test_unequal(self):
        cell1 = Cell(True, Coordinates(23, 42))
        cell2 = Cell(False, Coordinates(23, 42))
        assert cell1 != cell2


class TestCellStr(object):
    def test_none(self):
        assert str(Cell(None, ())) == ' '

    def test_false(self):
        assert str(Cell(False, ())) == '~'

    def test_true(self):
        assert str(Cell(True, ())) == 'X'
