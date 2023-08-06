import curses
import curses.panel
import pyperclip
import webbrowser

from .suppress import suppress_stdout_stderr


class CardPanel:
    def __init__(self):
        self.lines = curses.LINES
        self.win = curses.newwin(self.lines, curses.COLS - 1, 0, 0)
        self.panel = curses.panel.new_panel(self.win)
        self.panel.hide()
        self.selected = - 1

    def update(self, card):
        self.win.clear()
        self.selected = -1
        self.field_count = 0
        self.fields = None

        if card is not None:
            # find logest label
            field_idx = 0
            self.longest = 0
            self.fields = card['fields']
            self.field_count = 0

            for f in card['fields']:
                if f['value'] is None:
                    field_idx += 1
                    continue

                self.field_count += 1
                label_len = len(f['name'])
                if label_len > self.longest:
                    self.longest = label_len

                if (self.selected == -1 and
                        f['type'] in ('password', 'one_time_password', 'secret', 'pin')):
                    self.selected = field_idx

                field_idx += 1

            if self.field_count and self.selected == -1:
                self.selected = 0

            # print title
            y_pos = self.lines - self.field_count - 2
            self.win.addstr(y_pos, self.longest + 3, card['title'], curses.color_pair(3) | curses.A_BOLD)

            # print fields
            field_idx = 0
            for f in card['fields']:
                if f['value'] is None:
                    field_idx += 1
                    continue

                if f['type'] in ('password', 'one_time_password', 'secret'):
                    text = '**********'
                elif f['type'] == 'pin':
                    text = '***'
                else:
                    text = f['value']

                label = f['name']
                x_pos = self.longest - len(label) + 1
                y_pos += 1
                self.win.addstr(y_pos, x_pos, f'{label}:', curses.color_pair(4) | curses.A_BOLD)
                self.win.addstr(y_pos, self.longest + 3, text)

                if field_idx == self.selected:
                    self.win.addstr(y_pos, self.longest + 2, '>', curses.color_pair(1))

                field_idx += 1

        self.panel.top()

    def next(self):
        if not self.field_count:
            return

        y_pos = self.lines - self.field_count + self.selected - 1
        self.win.addstr(y_pos, self.longest + 2, ' ', curses.color_pair(1))

        y_pos += 1
        self.selected += 1
        if self.selected >= self.field_count:
            self.selected = 0
            y_pos = self.lines - self.field_count - 1

        self.win.addstr(y_pos, self.longest + 2, '>', curses.color_pair(1))

    def prev(self):
        if not self.field_count:
            return

        y_pos = self.lines - self.field_count + self.selected - 1
        self.win.addstr(y_pos, self.longest + 2, ' ', curses.color_pair(1))

        y_pos -= 1
        self.selected -= 1
        if self.selected < 0:
            self.selected = self.field_count - 1
            y_pos = self.lines - 2

        self.win.addstr(y_pos, self.longest + 2, '>', curses.color_pair(1))

    def handle_input(self, c):
        if c == ord('x'):
            return 'exit'

        if c in (27, ord('q')):
            self.panel.hide()
            return 'hide'

        elif c in (ord('k'), curses.KEY_UP):
            self.prev()

        elif c in (ord('j'), curses.KEY_DOWN):
            self.next()

        elif c in (10, 13, curses.KEY_ENTER):
            if self.selected != -1:
                field = self.fields[self.selected]
                if field['type'] == 'website':
                    with suppress_stdout_stderr():
                        webbrowser.open(field['value'])
                else:
                    pyperclip.copy(field['value'])

        return None
