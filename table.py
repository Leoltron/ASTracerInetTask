# !/usr/bin/env python3


def print_table(table: list):
    columns_length = [0] * max(len(row) for row in table)
    for i in range(len(columns_length)):
        columns_length[i] = max(
            len(row[i]) for row in table if i < len(row)) + 3
    format_string = ''.join("{:%d}" % l for l in columns_length)
    print("\n".join(
        [format_string.format(
            *(row + ('',) * (len(columns_length) - len(row))))
            for row in table]))
