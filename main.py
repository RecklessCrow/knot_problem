import numpy as np


FILE = 'input.txt'


def get_matrix():
    matrix = []

    with open(FILE) as f:
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
            reverse = False
            start = puzzle_pos[positions[0]]
            if len(positions) > 1:
                end = puzzle_pos[positions[1]]
                return start, end, row, reverse
        else:
            end = puzzle_pos[positions[0]]
            return start, end, row, reverse

    return None, None, None, None


# useing gauss code
def puzzle_solver(puzzle):
    crosses = ""

    start, end, row, reverse = find_start_end(puzzle)

    row_idx, col_idx = start
    pos = (row_idx, col_idx)

    while pos != end:
        char = puzzle[pos]

        if row:
            if char == 'H':
                crosses += 'H'
            elif char == 'I':
                crosses += 'I'

            if char == '+':
                row = False
                if puzzle[row_idx - 1, col_idx] == '|':
                    reverse = True
                    row_idx -= 1
                else:
                    reverse = False
                    row_idx += 1
            else:
                col_idx += 1 if not reverse else -1

        else:
            if char == 'H':
                crosses += 'I'
            elif char == 'I':
                crosses += 'H'

            if char == '+':
                row = True
                if puzzle[row_idx, col_idx - 1] == '-':
                    reverse = True
                    col_idx -= 1
                else:
                    reverse = False
                    col_idx += 1
            else:
                row_idx += 1 if not reverse else -1

        pos = (row_idx, col_idx)

    return crosses


if __name__ == '__main__':
    m = get_matrix()
    for idx, puzzle in enumerate(m):
        crosses = puzzle_solver(np.array(puzzle))
        knots = 'IHI' in crosses or 'HIH' in crosses
        output = f'Case {idx + 1}: {"knotted" if knots else "straightened"}'
        print(output)
