import numpy as np


def get_matrix(filename):
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

    return [m for m in matrix if m]


def find_start_end(puzzle):
    result = np.where(puzzle == '-')
    puzzle_pos = list(zip(result[0], result[1]))
    start = None
    end = None

    if 0 in result[1]:
        positions = np.where(result[1] == 0)[0]

        row = True
        reverse = False

        start = puzzle_pos[positions[0]]

        if len(positions) > 1:
            end = puzzle_pos[positions[1]]
            return start, end, row, reverse

    if len(puzzle[0]) - 1 in result[1]:
        positions = np.where(result[1] == len(puzzle[0]) - 1)[0]

        if start is None:
            row = True
            reverse = True
            start = puzzle_pos[positions[0]]
            if len(positions) > 1:
                end = puzzle_pos[positions[1]]
                return start, end, row, reverse
        else:
            end = puzzle_pos[positions[0]]
            return start, end, row, reverse

    result = np.where(puzzle == '|')
    puzzle_pos = list(zip(result[0], result[1]))

    if 0 in result[0]:
        positions = np.where(result[0] == 0)[0]

        if start is None:
            row = False
            reverse = False
            start = puzzle_pos[positions[0]]
            if len(positions) > 1:
                end = puzzle_pos[positions[1]]
                return start, end, row, reverse
        else:
            end = puzzle_pos[positions[0]]
            return start, end, row, reverse

    if len(puzzle) - 1 in result[0]:
        positions = np.where(result[0] == len(puzzle) - 1)[0]

        if start is None:
            row = False
            reverse = True
            start = puzzle_pos[positions[0]]
            if len(positions) > 1:
                end = puzzle_pos[positions[1]]
                return start, end, row, reverse
        else:
            end = puzzle_pos[positions[0]]
            return start, end, row, reverse

    return None, None, None, None


def generate_gauss_code(puzzle):
    cross_dict = {}
    cross_counter = 1
    crosses = []

    start, end, row, reverse = find_start_end(puzzle)

    row_idx, col_idx = start
    pos = (row_idx, col_idx)

    while pos != end:
        char = puzzle[pos]

        if row:
            if char == 'H' or char == 'I':
                if pos not in cross_dict:
                    cross_dict[pos] = cross_counter
                    cross_counter += 1
                val = cross_dict[pos] if char == 'H' else -cross_dict[pos]
                crosses.append(val)

            if char == '+':
                row = False
                if puzzle[row_idx - 1, col_idx] in ['|', 'H', 'I']:
                    reverse = True
                    row_idx -= 1
                else:
                    reverse = False
                    row_idx += 1
            else:
                col_idx += 1 if not reverse else -1

        else:
            if char == 'H' or char == 'I':
                if pos not in cross_dict:
                    cross_dict[pos] = cross_counter
                    cross_counter += 1
                val = -cross_dict[pos] if char == 'H' else cross_dict[pos]
                crosses.append(val)

            if char == '+':
                row = True
                if puzzle[row_idx, col_idx - 1] in ['-', 'H', 'I']:
                    reverse = True
                    col_idx -= 1
                else:
                    reverse = False
                    col_idx += 1
            else:
                row_idx += 1 if not reverse else -1

        pos = (row_idx, col_idx)

    return crosses


def simplify_code(code):
    idx = 0

    while idx < len(code) - 1:
        a = code[idx]
        b = code[idx + 1]

        if abs(a) == abs(b):
            del code[code.index(a)]
            del code[code.index(b)]
            idx = 0
            continue

        if np.sign(a) == np.sign(b):
            temp = ','.join([str(number) for number in code[idx + 2:]])

            if f'{-a},{-b}' in temp or f'{-b},{-a}' in temp:
                del code[code.index(a)]
                del code[code.index(b)]
                del code[code.index(-a)]
                del code[code.index(-b)]
                idx = 0
                continue

        idx += 1


def solver(code):
    print(code)
    return 'knotted' if code else 'straightened'


if __name__ == '__main__':
    from time import time

    filename = 'Test.dat'
    timer = True

    m = get_matrix(filename)
    for idx, puzzle in enumerate(m):
        start = time()
        puzzle = np.array(puzzle)
        gauss_code = generate_gauss_code(puzzle)
        simplify_code(gauss_code)
        solution = solver(gauss_code)
        end = time()

        output = f'Case {idx:2}: {solution:15} | {end - start:10f} ms' if timer else f'Case {idx:2}: {solution}'

        print(output)
