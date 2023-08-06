import os
import sys
import curses
import curses.panel
import getpass

from xml.etree import ElementTree

from .version import __version__
from .cardlist import CardList
from .cardpanel import CardPanel
from .database import read_sic_db
from .watcher import ActivityWatcher


def error(msg):
    print(f'\033[1;31m{msg}\033[0m')


def warning(msg):
    print(f'\033[1;33m{msg}\033[0m')


def load_db(filename):
    if filename[0] == '~':
        filename = filename.replace('~', os.environ['HOME'], 1)

    if not os.path.isfile(filename):
        error(f'File "{filename}" not found')
        return None

    retry_count = 0
    while True:
        try:
            database = read_sic_db(filename, getpass.getpass())
            break

        except Exception as err:
            msg = str(err)
            if ('unpack requires a buffer of' in msg or
                'Incorrect AES key length' in msg):
                if retry_count < 3:
                    warning('Invalid password, try again')
                    retry_count += 1
                else:
                    error('Too many invalid passwords')
                    return None
            else:
                error(f'Unable to decrypt database: {err}')
                return None

    cards = []
    for card in ElementTree.fromstring(database):
        # skip labels and ghosts
        if 'title' not in card.attrib:
            continue

        card_obj = {'title': card.attrib['title'], 'fields': []}

        for field in card:
            # skip comments, files, etc...
            if 'name' not in field.attrib or 'type' not in field.attrib:
                continue

            card_obj['fields'].append({
                'name': field.attrib['name'],
                'type': field.attrib['type'],
                'value': field.text
            })

        cards.append(card_obj)

    return cards

def start_curses_cli(scr, cards):
    watcher = ActivityWatcher(180)
    watcher.start()

    card_list = CardList(scr, cards)
    card_panel = CardPanel()

    scr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)

    prompt_pos = curses.LINES - 1
    scr.addstr(prompt_pos, 0, '>', curses.color_pair(2))

    card_showing = False
    scr.move(prompt_pos, 2)
    query = ''

    while True:
        curses.panel.update_panels()
        scr.refresh()

        c = scr.getch()
        watcher.keep_alive()

        if card_showing:
            action = card_panel.handle_input(c)
            if action == 'hide':
                card_showing = False

            elif action == 'exit':
                break

        else:
            action = card_list.handle_input(c)
            if action == 'exit':
                break

            elif action == 'sel_next':
                card_list.next()

            elif action == 'sel_prev':
                card_list.prev()

            elif action == 'show_card':
                card = card_list.get_selected()
                card_panel.update(card)
                card_showing = True

            elif action == 'clear':
                qlen = len(query)
                scr.addstr('{back}{blank}{back}'.format(blank=' ' * qlen, back='\b' * qlen))
                query = ''
                card_list.filter(query)

            elif action == 'del_char':
                if query:
                    scr.addstr('\b \b')
                    query = query[0:-1]
                    card_list.filter(query)

            elif action == 'add_char':
                scr.addch(c)
                query += chr(c)
                card_list.filter(query)

    watcher.stop()


def header():
    print(f'sicsearch v{__version__} - Safe in Cloud DB Search\n')


def usage():
    print("""Usage:
    sicsearch <database>
""")

def main():
    try:
        header()

        if len(sys.argv) != 2:
            usage()
            error('No database specified')
            return 1

        cards = load_db(sys.argv[1])

        if not cards:
            return 1

        os.environ.setdefault('ESCDELAY', '25')
        curses.wrapper(start_curses_cli, cards)
        return 0

    except KeyboardInterrupt:
        return 1


if __name__ == '__main__':
    main()
