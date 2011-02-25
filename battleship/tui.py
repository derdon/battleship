import string
from itertools import imap

from texttable import Texttable
import urwid

import battleship
import battleship.players


A_TO_J = string.ascii_uppercase[:10]


def format_field(field):
    table = Texttable()
    table.add_row([' '] + list(A_TO_J))
    for row_number, row in enumerate(field):
        formatted_row_number = '%2d' % (row_number + 1)
        table.add_row([formatted_row_number] + map(str, row))
    return table.draw()


class BattleshipDisplay(object):
    BUTTON_LABEL_PREFIX = '< '
    BUTTON_LABEL_SUFFIX = ' >'
    BASE_CELL_WIDTH_LENGTH = len(BUTTON_LABEL_PREFIX + BUTTON_LABEL_SUFFIX)

    def __init__(self):
        self.player = battleship.players.Player()
        self.opponent = battleship.players.Player(self.player.own_field)

        # create the user's field, add a caption on top of it and put these two
        # widgets into one Pile to stack them vertically
        self.users_field = urwid.Text(
            format_field(self.player.own_field), wrap='clip')
        users_field_caption = urwid.Text('Your field:')
        self.users_field_pile = urwid.Pile([
            users_field_caption, self.users_field])

        # the same happens with the opponent's field
        self.opponents_field = urwid.Text(
            format_field(self.player.opponents_field), wrap='clip')
        opponents_field_caption = urwid.Text('Opponent\'s field:')
        self.opponents_field_pile = urwid.Pile(
            [opponents_field_caption, self.opponents_field])

        self.add_ships_randomly_button = urwid.Button(
            'add ships randomly',
            on_press=self.add_ships_randomly)
        self.add_new_ship_manually_button = urwid.Button('add new ship')

        initial_buttons = [
            self.add_ships_randomly_button,
            self.add_new_ship_manually_button]

        actions_caption = urwid.Text('Actions:')
        largest_button_label_width = max(
            imap(self.get_button_label_length, initial_buttons))
        cell_width = largest_button_label_width + self.BASE_CELL_WIDTH_LENGTH
        self.actions = urwid.GridFlow(
            initial_buttons, cell_width, 1, 1, 'left')
        self.actions_pile = urwid.Pile([actions_caption, self.actions])

    @property
    def fields(self):
        return urwid.Columns([
            self.users_field_pile,
            self.opponents_field_pile])

    @property
    def main_layout(self):
        return urwid.Pile([self.actions_pile, self.fields])

    @property
    def filler(self):
        return urwid.Filler(self.main_layout, 'top')

    @property
    def loop(self):
        return urwid.MainLoop(
            self.filler, unhandled_input=self.unhandled_input)

    def main(self):
        self.loop.run()

    def unhandled_input(self, input):
        if input in ('q', 'Q', 'esc'):
            raise urwid.ExitMainLoop()

    def get_button_label_length(self, button):
        return len(button.label)

    def add_ships_randomly(self, button):
        add_ship = self.player.add_ship_randomly
        add_ship(3)
        for length in xrange(2, 6):
            add_ship(length)
        self.reload_own_field()
        # TODO: remove the button which is connected to this callback
        #self.add_ships_randomly_button.

    def reload_own_field(self):
        self.update_field(self.player.own_field, True)

    def update_field(self, field, is_users_field):
        new_formatted_field = format_field(field)
        if is_users_field:
            self.users_field.set_text(new_formatted_field)
        else:
            self.opponents_field.set_text(new_formatted_field)


def main():
    with battleship.log_handler.applicationbound():
        BattleshipDisplay().main()

if __name__ == '__main__':
    main()
