import curses
import curses.panel

from .fzmatch import fzmatch


class CardList:
    def __init__(self, scr, data):
        self.scr = scr
        self.lines = curses.LINES - 1
        self.win = curses.newwin(self.lines, curses.COLS - 1, 0, 0)
        self.panel = curses.panel.new_panel(self.win)
        self.data = data
        self.list = None
        self.selected = -1

    def filter(self, text):
        self.list = []
        if text:
            for card in self.data:
                match, score = fzmatch(card['title'], text)
                if match:
                    self.list.append({'card': card, 'match': match, 'score': score})

                elif len(text) >= 3:
                    for field in card['fields']:
                        if ('value' in field and field['value'] and
                                text.lower() in field['value'].lower()):
                            self.list.append({
                                'card': card,
                                'match': (' ' * len(card['title'])) + ' (' + field['name'] + ')',
                                'score': 1500 - abs(len(field['value']) - len(text))
                            })

        if len(self.list):
            self.selected = 0
            self.list.sort(reverse=True, key=lambda x: x['score'])
        else:
            self.selected = -1

        self.update_window()

    def update_window(self):
        self.win.clear()

        if self.list is None:
            return

        first_line = self.lines - 1
        y_pos = first_line
        for item in self.list:
            if first_line - y_pos == self.selected:
                self.win.addstr(y_pos, 0, '>', curses.color_pair(1))

            self.win.addstr(y_pos, 2, item['card']['title'])

            title_len = len(item['card']['title']) + 2
            curr_color = 1
            x_pos = 1
            for ch in item['match']:
                x_pos += 1
                if x_pos >= title_len:
                    curr_color = 5
                if ch != ' ':
                    self.win.addstr(y_pos, x_pos, ch, curses.color_pair(curr_color))

            y_pos -= 1
            if y_pos < 0:
                break

    def get_selected(self):
        if self.selected == -1:
            return None
        return self.list[self.selected]['card']

    def next(self):
        if self.selected != -1 and self.selected + 1 < len(self.list):
            self.win.addstr(self.lines - 1 - self.selected, 0, ' ')
            self.selected += 1
            self.win.addstr(self.lines - 1 - self.selected, 0, '>', curses.color_pair(1))

    def prev(self):
        if self.selected != -1 and self.selected > 0:
            self.win.addstr(self.lines - 1 - self.selected, 0, ' ')
            self.selected -= 1
            self.win.addstr(self.lines - 1 - self.selected, 0, '>', curses.color_pair(1))

    def handle_input(self, c):
        if c == 27:  # ALT seq
            key = self.scr.getch()
            if key in (ord('x'), ord('q')):
                return 'exit'

            elif key in (8, curses.KEY_BACKSPACE, ord('h')):
                return 'clear'

            elif key == ord('k'):
                return 'sel_next'

            elif key == ord('j'):
                return 'sel_prev'

        elif c == curses.KEY_UP:
            return 'sel_next'

        elif c == curses.KEY_DOWN:
            return 'sel_prev'

        elif c in (10, 13, curses.KEY_ENTER):
            return 'show_card'

        elif c in (8, curses.KEY_BACKSPACE):
            return 'del_char'

        elif c >= 32 and c <=126:
            return 'add_char'

        return None
