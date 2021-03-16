import numpy as np


def parse_puzzles(filename):
    matrix = []

    with open(filename) as f:
        puzzle = []

        for line in f:
            row = list(line.strip('\n'))
            if not row[0].isdigit():
                puzzle.append(row)
            else:
                matrix.append(puzzle)
                puzzle = []

        matrix.append(puzzle)

    return [np.array(m) for m in matrix if m]


def find_start_end(puzzle):
    start = None
    row = True
    reverse = False

    first_col = puzzle[:, 0]
    if '-' in first_col:
        start = np.where(first_col == '-')[0][0], 0

    last_col = puzzle[:, -1]
    if '-' in last_col:
        if start is None:
            start = np.where(last_col == '-')[0][0], len(puzzle[0]) - 1
            reverse = True
        else:
            end = np.where(last_col == '-')[0][0], len(puzzle[0]) - 1,
            return start, end, row, reverse

    first_row = puzzle[0]
    if '|' in first_row:
        if start is None:
            start = 0, np.where(first_row == '|')[0][0]
            row = False
        else:
            end = 0, np.where(first_row == '|')[0][0]
            return start, end, row, reverse

    last_row = puzzle[-1]
    if '|' in last_row:
        end = len(puzzle) - 1, np.where(last_row == '|')[0][0]
        return start, end, row, reverse

    raise AttributeError('No start or end position exists')


def generate_gauss_code(puzzle):
    cross_dict = {}
    cross_counter = 1
    crosses = []

    start, end, row, reverse = find_start_end(puzzle)

    row_idx, col_idx = start
    pos = (row_idx, col_idx)

    while pos != end:
        char = puzzle[pos]

        if char == 'H' or char == 'I':
            if pos not in cross_dict:
                cross_dict[pos] = cross_counter
                cross_counter += 1

            if row:
                val = cross_dict[pos] if char == 'H' else -cross_dict[pos]
            else:
                val = -cross_dict[pos] if char == 'H' else cross_dict[pos]

            crosses.append(val)

        if char == '+':
            if row:
                if puzzle[row_idx - 1, col_idx] in ['|', 'H', 'I']:
                    reverse = True
                    row_idx -= 1
                else:
                    reverse = False
                    row_idx += 1
            else:
                if puzzle[row_idx, col_idx - 1] in ['-', 'H', 'I']:
                    reverse = True
                    col_idx -= 1
                else:
                    reverse = False
                    col_idx += 1

            row = not row

        else:
            if row:
                col_idx += 1 if not reverse else -1
            else:
                row_idx += 1 if not reverse else -1

        pos = (row_idx, col_idx)

    return crosses


def simplify_code(code):
    idx = 0

    while idx < len(code) - 1:

        if len(code) <= 4:
            return []

        a = code[idx]
        b = code[idx + 1]

        if abs(a) == abs(b):  # single loop
            code.remove(a)
            code.remove(b)
            idx = 0
            continue

        if np.sign(a) == np.sign(b) and (f'{-a}, {-b}' in str(code) or f'{-b}, {-a}' in str(code)):  # double loop
            code.remove(a)
            code.remove(b)
            code.remove(-a)
            code.remove(-b)
            idx = 0
            continue

        idx += 1

    return code


def main():
    filename = 'test_inputs.txt'
    puzzles = parse_puzzles(filename)

    for idx, puzzle in enumerate(puzzles):
        gauss_code = generate_gauss_code(puzzle)
        gauss_code = simplify_code(gauss_code)
        knot_string = 'knotted' if gauss_code else 'straightened'
        print(f'Case {idx:2}: {knot_string}')


if __name__ == '__main__':
    main()
