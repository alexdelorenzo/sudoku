import math as m

def import_file(name="easy50.txt", delimiter="========"):
    grids = []
    with open(name, 'rb') as boards:
        grids = [row for row in boards if '=' not in row]
        grids = zip(*(iter(grids),) * 9)
    return grids

def import_string(string):
    parsed = [[int(i) for i in row.strip()] for row in string]
    return parsed

def sudoku_board(size=9):
    return [[None for none in xrange(size)] for row in xrange(size)]

def return_ledger(board):
    need_dict = {
                'row': [{y for y in xrange(1,10)} for x in xrange(9)],
                'col': [{y for y in xrange(1,10)} for x in xrange(9)],
                'box': {(x,y): {n for n in xrange(1,10)}
                                for x in xrange(3)
                                for y in xrange(3)}
                }
    poss = {'pts': possibities(board), 'need': need_dict}
    return poss
def possibities(board):
    posnum, length, width = \
            xrange(1,10), xrange(len(board)), xrange(len(board))
    poss = {(x,y): {p for p in posnum} for x in length for y in width}
    return poss


def calc_row(board, poss, index):
    x = index
    row = {board[x][y]
            for y in xrange(9)
            if board[x][y]}
    poss['need']['row'][index] -= row


def calc_column(board, poss, index):
    y = index
    column = {board[row][y]
            for row in xrange(9)
            if board[row][y]}
    poss['need']['col'][index] -= column


def calc_box(board, poss, index):
    x, y = index[0] * 3, index[1] * 3
    box = {board[row][col]
            for row in xrange(x, x + 3)
            for col in xrange(y, y + 3)
            if board[row][col]}
    poss['need']['box'][index] -= box


def update_poss(board, poss, point, box_pts):
    x, y = point
    calc_row(board, poss, x)
    calc_column(board, poss, y)
    calc_box(board, poss, box_pts)


def poss_point(board, poss, point):
    x, y = point
    in_box = (int(m.floor(x / 3.0)), int(m.floor(y / 3.0)))

    update_poss(board, poss, point, in_box)

    if board[x][y]:
        poss['pts'][point] = set()
        return

    rows, cols, boxes = poss['need']['row'][x], poss['need']['col'][y], \
        poss['need']['box'][in_box]

    intersection = rows & cols & boxes
    poss['pts'][point] = intersection


def poss_grid(board, poss):
    for point in poss['pts']:
        poss_point(board, poss, point)


def constraints(board, poss):
    def process_nums(board, poss, point, nums):
        for num, occurs in nums.items():
            if len(occurs) == 1:
                point = occurs.pop()
                set_sq(board, point, num)
                poss_point(board, poss, point)

    def point_has_one_possible_val(board, poss, point):
        possible = poss['pts'][point]
        if len(possible) == 1:
            set_sq(board, point, possible.pop())
            poss_point(board, poss, point)

    def unit_has_place_for_val(board, poss, point):
        rows, cols, boxes, pts= poss['need']['row'], \
            poss['need']['col'], poss['need']['box'], \
            poss['pts']
        for row, unit in enumerate(rows):
            pts_in_unit = [(row,y) for y in xrange(9)]
            nums = {num: [pt
                        for pt in pts_in_unit
                        if num in pts[pt]] for num in unit}
            process_nums(board, poss, point, nums)

        for col, unit in enumerate(cols):
            pts_in_unit = [(x,col) for x in xrange(9)]
            nums = {num: [pt
                        for pt in pts_in_unit
                        if num in pts[pt]] for num in unit}
            process_nums(board, poss, point, nums)

        for box in boxes:
            x, y = point
            x, y = int(m.floor(x / 3.0)), int(m.floor(y / 3.0))
            pts_in_unit = set({(row, col)
                        for row in xrange(x, x + 3)
                        for col in xrange(y, y + 3)})
            nums = {num: [pt
                    for pt in pts_in_unit
                    if num in pts[pt]] for num in unit}
            for num, occurs in nums.items():
                if len(occurs) == 1:
                    point = occurs.pop()
                    set_sq(board, point, num)
                    poss_point(board, poss, point)

    for point in poss['pts']:
        point_has_one_possible_val(board, poss, point)
        unit_has_place_for_val(board, poss, point)

def set_sq(board, point, val):
    x, y = point
    board[x][y] = val
