#!/usr/bin/env python
# coding: utf-8
"""
Usage:
    note [options] [-]
    note [options] <file>
    note --delete=<number>

Options:
    -i, --index=<number>    note index
    -d, --delete=<number>   delete note(s) of this index
    -c, --color=<color>     note color
    -l, --list              list all notes
"""
# $ sqlite3 .local/share/jolla-notes/QML/OfflineStorage/Databases/8b63c31a7656301b3f7bcbbfef8a2b6f.sqlite
# CREATE TABLE notes (pagenr INTEGER, color TEXT, body TEXT);
# CREATE TABLE next_color_index (value INTEGER);
# sqlite> insert into notes (body) values ("blabla");
# sqlite> .quit

import sqlite3
import atexit
import os
import sys
import textwrap
import logging
import random
from docpie import docpie, logger as pielog

__version__ = '0.0.5'
__author__ = 'TylerTemp <tylertempdev@gmail.com>'

if sys.version_info[0] < 3:
    from codecs import open

try:
    import io
except ImportError:

    def decoded_stdin():
        return sys.stdin

else:

    def decode_stdin():
        return io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


logging.basicConfig(level=logging.DEBUG)
pielog.setLevel(logging.WARNING)


logger = logging.getLogger('jolla-note-cli')

connector = sqlite3.connect(os.path.expanduser(
    '~/.local/share/jolla-notes/QML/OfflineStorage/Databases/'
    '8b63c31a7656301b3f7bcbbfef8a2b6f.sqlite'))

cursor = connector.cursor()

commit = connector.commit


colors = (
    {'color': '#cc0000', 'index': 1, 'name': 'red'},
    {'color': '#cc7700', 'index': 2, 'name': 'orange'},
    {'color': '#ccbb00', 'index': 3, 'name': 'yellow'},
    {'color': '#88cc00', 'index': 4, 'name': None},
    {'color': '#00b315', 'index': 5, 'name': 'green'},
    {'color': '#00bf9f', 'index': 6, 'name': None},
    {'color': '#005fcc', 'index': 7, 'name': 'indigo'},
    {'color': '#0016de', 'index': 8, 'name': 'blue'},
    {'color': '#bb00cc', 'index': 9, 'name': 'purple'},
    {'color': '#ffffff', 'index': None, 'name': 'white'},
    {'color': '#000000', 'index': None, 'name': 'black'}
)


@atexit.register
def close():
    cursor.close()
    connector.close()


cursor.execute("SELECT count(*) FROM sqlite_master "
               "WHERE type='table' AND name='next_color_index'")

has_index_table = cursor.fetchone() == (0,)


def get_color(**kwargs):
    for color in colors:
        for wanted_key, wanted_value in kwargs.items():
            if color.get(wanted_key, None) != wanted_value:
                break
        else:
            return color
    else:
        return None


def insert(**kwargs):
    sql = 'INSERT INTO notes ({cols}) VALUES ({vals})'

    val_lis = list(kwargs.values())
    placeholder = ','.join('?' for _ in val_lis)
    formatted_sql = sql.format(cols=','.join(kwargs), vals=placeholder)
    logger.debug(formatted_sql)
    logger.debug(val_lis)

    cursor.execute(formatted_sql, val_lis)
    commit()

    print(cursor.fetchall())


def delete(index):
    cursor.execute('DELETE FROM notes WHERE pagenr=?', (index,))
    commit()
    print(cursor.fetchall())


def get_color_next_index():
    cursor.execute('SELECT * FROM next_color_index ORDER BY value')
    result = cursor.fetchone()
    return result[0] if result is not None else None


def set_color_next_index(index):
    cursor.execute('DELETE FROM next_color_index')
    cursor.execute('INSERT INTO next_color_index (value) VALUES (?)', (index,))
    commit()
    print(cursor.fetchall())


def get_page_index():
    cursor.execute('SELECT max(pagenr) FROM notes')
    result = cursor.fetchone()
    return result[0] if result else 0


def list_all():
    cursor.execute('SELECT * FROM notes ORDER BY pagenr')

    for index, color, content in cursor.fetchall():
        index_pref = '%s. ' % index
        indent = len(index_pref)
        if color is not None:
            color_detail = get_color(color=color)
            if color_detail is not None:
                color = color_detail.get('name', None)
                if 'index' in color_detail:
                    color = '(%s) %s' % (color_detail['index'], color)

        print('%s[%s]' % (index_pref, color))
        try:
            print('\n'.join(
                    textwrap.wrap(content,
                                  initial_indent=' ' * indent,
                                  subsequent_indent=' ' * indent)))
        except UnicodeEncodeError:
            print(content.encode('utf-8'))
        print('')


def get_data(file=None):
    if file is None:
        return decode_stdin().read()
    elif hasattr(file, 'read'):
        return file.read()
    else:
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()


def main(argv=None):
    args = docpie(__doc__, argv=argv)
    if args['--list']:
        list_all()
        return 0
    elif args['--delete']:
        to_delete = int(args['--delete'])
        delete(to_delete)
        return 0
    else:
        fname = None if args['-'] else args['<file>']
        content = get_data(fname)
        raw_color = args['--color']
        if raw_color is None:
            if has_index_table:
                color_index = get_color_next_index() or 1
                color = get_color(index=color_index)['color']
            else:
                color_index = random.choice(colors)['color']
        elif raw_color.startswith('#'):
            color = raw_color
        elif raw_color.isdigit():
            color = get_color(index=int(raw_color))['color']
        else:
            color = get_color(name=raw_color)['color']
        raw_pagenr = args['--index']
        if raw_pagenr is None:
            pagenr = get_page_index() + 1
        else:
            pagenr = int(raw_pagenr)

        insert(color=color, body=content, pagenr=pagenr)
        return 0


if __name__ == '__main__':
    sys.exit(main())
