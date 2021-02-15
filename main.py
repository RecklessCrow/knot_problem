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


# useing gauss code
def puzzle_solver(puzzle):
    row_idx = int(np.where(puzzle[:, 0] == '-')[0])
    col_idx = 0
    crosses = ""

    row = True
    reverse = False

    try:
        while True:
            pos = (row_idx, col_idx)

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
    except IndexError:
        pass

    return crosses


if __name__ == '__main__':
    m = get_matrix()
    for idx, puzzle in enumerate(m):
        crosses = puzzle_solver(np.array(puzzle))
        knots = 'IHI' in crosses or 'HIH' in crosses
        output = f'Case {idx + 1}: {"knotted" if knots else "straightened"}'
        print(output)
