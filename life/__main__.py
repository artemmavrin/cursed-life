"""Play Conway's Game of Life in a curses window."""

import argparse
import curses
import itertools

from .life import Life, Geometry, GEOMETRIES

# Dead cells are marked by the space character: ' '
_CH_DEAD = chr(32)

# Living cells are marked by the character '@'
_CH_ALIVE = chr(64)

# Program description
_DESCRIPTION = "Conway's Game of Life."

# Command line argument parsing
parser = argparse.ArgumentParser(description=_DESCRIPTION)

parser.add_argument("--geometry", type=str, choices=GEOMETRIES,
                    default=Geometry.TORUS, help="specify the board geometry")
parser.add_argument("--prob", type=float, default=0.25,
                    help="probability of a cell starting out alive")
parser.add_argument("--seed", type=int, default=None,
                    help="pseudo-random number generator seed")
parser.add_argument("--delay", type=int, default=60,
                    help="number of milliseconds to pause between states")


def main(stdscr, *, geometry, prob, seed, delay):
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
    """
    # Clear the screen
    stdscr.clear()

    # Don't wait for the user to enter anything
    stdscr.timeout(0)

    # Hide the cursor
    curses.curs_set(0)

    # Get the full dimensions of the screen
    n_rows, n_cols = stdscr.getmaxyx()

    # Create a Game of Life instance to be played
    life = Life(n_rows, n_cols, geometry=geometry, prob=prob, seed=seed)
    life.randomize()

    while True:
        try:
            for row, col in itertools.product(range(n_rows), range(n_cols)):
                cell_marker = _CH_ALIVE if life.state[row, col] else _CH_DEAD
                try:
                    stdscr.addch(row, col, cell_marker)
                except curses.error:
                    pass
            stdscr.refresh()
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
                   delay=args.delay)
