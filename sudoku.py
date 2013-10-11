from pprint import pprint as p
import pyglet
from sudoku import sudoku_solver_naive as s

x, y = 10, 10


scale = 10
x *= scale
y *= scale

red, blue, green, alpha = \
        (
        lambda tup, magnitude: (tup[0] + magnitude, tup[1], tup[2], tup[3]),
        lambda tup, magnitude: (tup[0], tup[1], tup[2] + magnitude, tup[3]),
        lambda tup, magnitude: (tup[0], tup[1] + magnitude, tup[2], tup[3]),
        lambda tup, magnitude: (tup[0], tup[1], tup[2], tup[3] + magnitude)
        )


black = 0.0, 0.0, 0.0, 1.0
white = red(green(blue(black, 1.0), 1.0), 1.0)
color = white
set_live_color = pyglet.gl.glColor4f

set_live_color(*color)

four, gl_flag, indices = 4, 'v2i', (0, 1, 2, 0, 2, 3)
purple = red(blue(alpha(black, 0.5), 0.5), 0.5)
window = pyglet.window.Window(width=x, height=y)
gl_draw_sq = pyglet.graphics.draw_indexed

def draw_square(point, value, size=1):
    four, gl_flag, indices = 4, 'v2i', (0, 1, 2, 0, 2, 3)
    x, y = point[0] * size, point[1] * size
    x_size, y_size = x + size, y + size
    vertices = x,y, x_size,y, x_size,y_size, x,y_size
    gl_draw_sq(four, pyglet.gl.GL_TRIANGLES, indices, (gl_flag, vertices))

def on_draw(board, poss):
    for point, guesses in poss['pts'].items():
        if not guesses:
            x, y = point
            print point
            gl_draw_sq(point, board[x][y], scale)


def main():
    boards = s.import_file()
    boards = [s.import_string(board) for board in boards]
    def coord_board():
        board[2][0] = 7
        board[0][1] = 8
        board[1][1] = 5
        board[2][1] = 3

        board[4][0] = 6
        board[5][0] = 1
        board[4][2] = 9

        board[7][0] = 8
        board[6][1] = 9
        board[7][1] = 1
        board[8][2] = 5

        coords = (1,3,4), (2,3,1), (2,4,3), (0,5,6), (2,5,2), \
                (3,4,2), (4,4,5), (5,4,4), \
                (6,3,8), (8,3,3), (7,4,6), (6,5,5), (7,5,4), \
                (0,6,1), (1,7,8), (2,7,4), (1,8,2), \
                (4,6,4),  (3,8,6), (4,8,1), \
                (6,7,6), (7,7,5), (8,7,1), (7,8,9)

        for coord in coords:
            s.set_sq(board, coord[:2], coord[2])
    for board in boards:
        poss = s.return_ledger(board)
        s.poss_grid(board, poss)
#    s.constraints(board, poss)
        s.constraints(board, poss)
        s.constraints(board, poss)
        s.constraints(board, poss)
        p(board)
        #p(poss['pts'])
        #p(poss['need'])
        #print poss['pts'][(0,0)]
        #print poss['need']['row'][0]
        #print poss['need']['col'][0]

        #pyglet.clock.schedule(on_draw, board, poss)
        #pyglet.app.run()

if __name__ == "__main__":
    main()
