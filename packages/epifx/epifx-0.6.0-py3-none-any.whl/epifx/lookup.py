"""Lookup tables for model parameters."""

import codecs
import numpy as np
from . import obs


def lookup_table(filename, value_dtype='float', comment='#'):
    if comment is None:
        comment = '#'

    skip_lines = 1
    with codecs.open(filename, encoding='ascii') as f:
        cols = f.readline().strip().split()
        while len(cols) == 0 or cols[0].startswith(comment):
            cols = f.readline().strip().split()
            skip_lines += 1

    col_convs = {0: lambda s: obs.datetime_conv(s, encoding='ascii')}
    col_types = [(name, 'O' if ix == 0 else value_dtype)
                 for (ix, name) in enumerate(cols)]

    with codecs.open(filename, encoding='ascii') as f:
        try:
            tbl = np.loadtxt(f, skiprows=skip_lines, dtype=col_types,
                             converters=col_convs)
        except (TypeError, UnicodeDecodeError) as e:
            msg = "File '{}' contains non-ASCII text".format(filename)
            print(e)
            raise ValueError(msg)

    if len(tbl) == 0:
        raise ValueError("File '{}' contains no rows".format(filename))

    return Lookup(tbl)


class Lookup:
    def __init__(self, table):
        self.__table = table

    def value_count(self):
        # NOTE: ignore the first column, which contains the date/time.
        return len(self.__table.dtype.names) - 1

    def lookup(self, when):
        date_col = self.__table.dtype.names[0]
        ixs = np.where(self.__table[date_col] <= when)[0]
        if len(ixs) == 0:
            # No match, default to the earliest value.
            most_recent_row = 0
        else:
            most_recent_row = ixs[-1]
        values = self.__table[most_recent_row].tolist()[1:]
        return np.array(values)
