"""Play Conway's Game of Life in a curses window."""

import argparse
import curses
import curses.ascii
import itertools

from .life import Life, Geometry, GEOMETRIES

# Dead cells are marked by the space character: ' '
_CH_DEAD = chr(32)

# Living cells are marked by the character '@'
_CH_ALIVE = chr(64)

# Program name
_PROGRAM = "python -m life"

# Program description
_DESCRIPTION = "Conway's Game of Life on compact surfaces."

# Command line argument parsing
parser = argparse.ArgumentParser(prog=_PROGRAM, description=_DESCRIPTION)

parser.add_argument("--geometry", type=str, choices=GEOMETRIES,
                    default=Geometry.TORUS, help="specify the board geometry")
parser.add_argument("--prob", type=float, default=0.25,
                    help="probability of a cell starting out alive")
parser.add_argument("--seed", type=int, default=None,
                    help="pseudo-random number generator seed")
parser.add_argument("--delay", type=int, default=60,
                    help="number of milliseconds to pause between states")
parser.add_argument("--draw", action="store_true", help="draw the initial board before playing")


def draw_cell(screen, life, row, col):
    """Draw a cell on the life board."""
    cell_marker = _CH_ALIVE if life.state[row, col] else _CH_DEAD
    try:
        screen.addch(row, col, cell_marker)
    except curses.error:
        pass


def draw_board(screen, life):
    """Draw the entire game of life board."""
    for row, col in itertools.product(range(life.n_rows), range(life.n_cols)):
        draw_cell(screen, life, row, col)


def main(stdscr, *, geometry, prob, seed, delay, draw):
    """Game of Life driver function.

    Parameters
    ----------
    stdscr : curses.window
        The main curses window.

    geometry : str
        The Game of Life board geometry.

    prob : float
        Probability of a cell starting out alive.

    seed : int, array-like, or None
        Seed for the pseudo-random number generator.

    delay : int
        Number of milliseconds to pause between consecutive board states.

    draw : bool
        Whether to manually draw the initial board (if True) or randomly generate an initial board
        (if False).
    """
    # Clear the screen
    stdscr.clear()

    # Get the full dimensions of the screen
    n_rows, n_cols = stdscr.getmaxyx()

    # Create a Game of Life instance to be played
    life = Life(n_rows, n_cols, geometry=geometry, prob=prob, seed=seed)

    # Initialize the board
    if draw:
        # Make the cursor extra visible and put it in the center of the board.
        curses.curs_set(2)
        cursor_row = life.n_rows // 2 + 1
        cursor_col = life.n_cols // 2
        stdscr.move(cursor_row, cursor_col)

        while True:
            # Wait for input from the user.
            c = stdscr.getch()

            if curses.ascii.isblank(c):
                # Stop drawing when <Space> is pressed
                break
            elif curses.ascii.isspace(c):
                # If the user pressed <Enter>, toggle the cell under the cursor
                life.toggle_cell(cursor_row, cursor_col)
                draw_cell(stdscr, life, cursor_row, cursor_col)
            elif c == curses.KEY_UP:
                # Move the cursor up if possible
                if cursor_row > 0:
                    cursor_row -= 1
                else:
                    if life.geometry in (Geometry.TORUS, Geometry.KLEIN_BOTTLE):
                        cursor_row = life.n_rows - 1
                    elif life.geometry == Geometry.PROJECTIVE_PLANE:
                        cursor_row = life.n_rows - 1
                        cursor_col = life.n_cols - cursor_col - 1
                    else:
                        curses.flash()
            elif c == curses.KEY_DOWN:
                # Move the cursor down if possible
                if cursor_row < life.n_rows - 1:
                    cursor_row += 1
                else:
                    if life.geometry in (Geometry.TORUS, Geometry.KLEIN_BOTTLE):
                        cursor_row = 0
                    elif life.geometry == Geometry.PROJECTIVE_PLANE:
                        cursor_row = 0
                        cursor_col = life.n_cols - cursor_col - 1
                    else:
                        curses.flash()
            elif c == curses.KEY_LEFT:
                # Move the cursor left if possible
                if cursor_col > 0:
                    cursor_col -= 1
                else:
                    if life.geometry in (Geometry.CYLINDER, Geometry.TORUS):
                        cursor_col = life.n_cols - 1
                    elif life.geometry in (Geometry.MOBIUS_STRIP, Geometry.KLEIN_BOTTLE,
                                           Geometry.PROJECTIVE_PLANE):
                        cursor_col = life.n_cols - 1
                        cursor_row = life.n_rows - cursor_row - 1
                    else:
                        curses.flash()
            elif c == curses.KEY_RIGHT:
                # Move the cursor right if possible
                if cursor_col < life.n_cols - 1:
                    cursor_col += 1
                else:
                    if life.geometry in (Geometry.CYLINDER, Geometry.TORUS):
                        cursor_col = 0
                    elif life.geometry in (Geometry.MOBIUS_STRIP, Geometry.KLEIN_BOTTLE,
                                           Geometry.PROJECTIVE_PLANE):
                        cursor_col = 0
                        cursor_row = life.n_rows - cursor_row - 1
                    else:
                        curses.flash()
            elif curses.ascii.isalpha(c) and chr(c) in "rR":
                # If the user presses the 'R' key, randomize the board
                life.randomize()
                draw_board(stdscr, life)
            elif curses.ascii.isalpha(c) and chr(c) in "qQ":
                # If the user presses the 'Q' key, exit
                return
            elif c == curses.KEY_RESIZE:
                # If the user resizes the window, exit
                return
            else:
                # TODO: add more functionality (e.g., help menu)
                pass

            # Move the cursor to a potentially new location
            stdscr.move(cursor_row, cursor_col)
    else:
        # Bypass drawing the board manually
        life.randomize()

    # Hide the cursor
    curses.curs_set(0)

    # Don't wait for the user to enter anything
    stdscr.timeout(0)

    while True:
        try:
            draw_board(stdscr, life)
            curses.delay_output(delay)
            life.evolve()
            c = stdscr.getch()
            if c != -1:
                break
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    args = parser.parse_args()
    curses.wrapper(main, geometry=args.geometry, prob=args.prob, seed=args.seed,
                   delay=args.delay, draw=args.draw)
