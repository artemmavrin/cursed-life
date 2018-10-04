"""Play Conway's Game of Life in the terminal."""

import argparse
import curses
import enum
import itertools
import numbers
import warnings

import numpy as np
from scipy.signal import correlate

# Dead cells are marked by the space character: ' '
_CH_DEAD = chr(32)

# Living cells are marked by the character '@'
_CH_ALIVE = chr(64)

# Kernel for cross-correlation to determine the number of neighbors of a cell
_KERNEL = np.asarray([[1, 1, 1],
                      [1, 10, 1],
                      [1, 1, 1]])


@enum.unique
class Geometry(enum.Enum):
    """Enum representing the available geometries for a Game of Life board."""
    RECTANGLE = "rectangle"
    CYLINDER = "cylinder"
    TORUS = "torus"
    MOBIUS_STRIP = "Mobius strip"
    KLEIN_BOTTLE = "Klein bottle"
    PROJECTIVE_PLANE = "projective plane"


def _check_positive_int(value, name):
    """Check that a function parameter is a positive int.

    Parameters
    ----------
    value : object
        The value of the parameter which should be a positive int.

    name : str
        The name of the parameter in the calling function.

    Returns
    -------
    value : int
        The validated positive integer.

    Raises
    ------
    TypeError
        If `value` is not an integer.

    ValueError
        If `value` is not positive.
    """
    if isinstance(value, numbers.Integral):
        value = int(value)
        if value > 0:
            return value
        else:
            raise ValueError(f"Parameter '{name}' must be positive.")
    else:
        raise TypeError(f"Parameter '{name}' must be an integer.")


def _check_probability(value, name):
    """Check that a function parameter is a probability (a float in the interval
    [0, 1]).

    Parameters
    ----------
    value : object
        The value of the parameter which should be a probability.

    name : str
        The name of the parameter in the calling function.

    Returns
    -------
    value : int
        The validated probability.

    Raises
    ------
    TypeError
        If `value` is not a float.

    ValueError
        If `value` is not in the interval [0, 1].
    """
    if isinstance(value, numbers.Real):
        value = float(value)
        if 0. <= value <= 1.:
            return value
        else:
            raise ValueError(f"Parameter '{name}' must between 0 and 1.")
    else:
        raise TypeError(f"Parameter '{name}' must be a float.")


class Life:
    """Conway's Game of Life.

    This is a cellular automaton, introduced by John Conway [1]_, consisting of
    a discrete rectangular grid of "cells", each of which is in one of two
    states: alive or dead. The automaton evolves in discrete time according to
    the following rules:

    * If a cell is alive, then it remains alive in the next generation if it has
      two or three living neighbors; otherwise, it dies.
    * If a cell is dead, then it becomes alive in the next generation if it has
      three living neighbors; otherwise, it remains dead.

    Parameters
    ----------
    n_rows : int
        The number of rows in the cell grid.
    n_cols : int
        The number of columns in the cell grid.
    geometry : str, optional
        Specifies how the cells on the edges of the board should behave.
        Acceptable values are "rectangle", "cylinder", "torus", "Mobius strip",
        "Klein bottle", and "projective plane".
    seed : int, array-like, or None, optional
        Seed for a numpy.random.RandomState pseudo-random number generator.

    References
    ----------
    .. [1] Martin Gardner. "Mathematical Games – The fantastic combinations of
      John Conway's new solitaire game "life"". Scientific American. Volume 223,
      pp. 120–-123.
    """

    def __init__(self, n_rows, n_cols, *, geometry="torus", prob=0.5,
                 seed=None):
        self.n_rows = _check_positive_int(n_rows, "n_rows")
        self.n_cols = _check_positive_int(n_cols, "n_cols")
        self.prob = _check_probability(prob, "prob")
        self.geometry = Geometry(geometry)

        # Pseudo-random number generator
        self.rng = np.random.RandomState(seed)

        # Initialize the board
        self._padded_state = np.zeros(shape=(n_rows + 2, n_cols + 2),
                                      dtype=np.bool_)

        # TODO: this next line is unnecessary but removing it bothers PyCharm
        self.state = self.state

    @property
    def state(self):
        """Get the board state."""
        return self._padded_state[1:-1, 1:-1]

    @state.setter
    def state(self, new_state):
        """Set the board state."""
        self._padded_state[1:-1, 1:-1] = new_state
        self._update_padding()

    # Functions for manual state mutation

    def clear(self):
        """Kill every cell."""
        self.state = np.zeros(shape=(self.n_rows, self.n_cols), dtype=np.bool_)
        return self

    def randomize(self):
        """Randomly make each cell alive or dead."""
        self.state = self.rng.choice([False, True],
                                     p=[1 - self.prob, self.prob],
                                     size=(self.n_rows, self.n_cols))
        return self

    def toggle_cell(self, row, col):
        """Change the state of the cell at row `row` and columns `col`."""
        if not (0 <= row < self.n_rows and 0 <= col < self.n_cols):
            raise IndexError("Invalid row or column index.")
        self._padded_state[row + 1, col + 1] ^= True

    # State evolution functions

    def evolve(self):
        """Compute the next state using the current state."""
        with warnings.catch_warnings():
            warnings.simplefilter(action="ignore", category=FutureWarning)
            neighbors = correlate(self._padded_state, _KERNEL, mode="same")

        new_state = (neighbors == 12) | (neighbors == 13) | (neighbors == 3)
        self.state = new_state[1:-1, 1:-1]
        return self

    def _update_padding(self):
        """Update the padding of the board according to the board's geometry."""
        if self.geometry is Geometry.RECTANGLE:
            self._update_padding_rectangle()
        elif self.geometry is Geometry.CYLINDER:
            self._update_padding_cylinder()
        elif self.geometry is Geometry.TORUS:
            self._update_padding_torus()
        elif self.geometry is Geometry.MOBIUS_STRIP:
            self._update_padding_mobius_strip()
        elif self.geometry is Geometry.KLEIN_BOTTLE:
            self._update_padding_klein_bottle()
        elif self.geometry is Geometry.PROJECTIVE_PLANE:
            self._update_padding_projective_plane()
        else:
            # This should not be reachable!
            raise ValueError(f"Unsupported geometry: {self.geometry}")

    def _update_padding_rectangle(self):
        """Update the padding of a rectangle board."""
        self._padded_state[0, :] = 0
        self._padded_state[-1, :] = 0
        self._padded_state[:, 0] = 0
        self._padded_state[:, -1] = 0

    def _update_padding_cylinder(self):
        """Update the padding of a cylinder board."""
        self._padded_state[0, :] = 0
        self._padded_state[-1, :] = 0
        self._padded_state[1:-1, 0] = self.state[:, -1]
        self._padded_state[1:-1, -1] = self.state[:, 0]

    def _update_padding_torus(self):
        """Update the padding of a torus board."""
        # Non-corner edges
        self._padded_state[0, 1:-1] = self.state[-1, :]
        self._padded_state[-1, 1:-1] = self.state[0, :]
        self._padded_state[1:-1, 0] = self.state[:, -1]
        self._padded_state[1:-1, -1] = self.state[:, 0]

        # Corners
        self._padded_state[0, 0] = self.state[-1, -1]
        self._padded_state[0, -1] = self.state[-1, 0]
        self._padded_state[-1, 0] = self.state[0, -1]
        self._padded_state[-1, -1] = self.state[0, 0]

    def _update_padding_mobius_strip(self):
        """Update the padding of a Mobius strip board."""
        self._padded_state[0, :] = 0
        self._padded_state[-1, :] = 0
        self._padded_state[1:-1, 0] = self.state[::-1, -1]
        self._padded_state[1:-1, -1] = self.state[::-1, 0]

    def _update_padding_klein_bottle(self):
        """Update the padding of a Klein bottle board."""
        # Non-corner edges
        self._padded_state[0, 1:-1] = self.state[-1, :]
        self._padded_state[-1, 1:-1] = self.state[0, :]
        self._padded_state[1:-1, 0] = self.state[::-1, -1]
        self._padded_state[1:-1, -1] = self.state[::-1, 0]

        # Corners
        self._padded_state[0, 0] = self.state[0, -1]
        self._padded_state[0, -1] = self.state[0, 0]
        self._padded_state[-1, 0] = self.state[-1, -1]
        self._padded_state[-1, -1] = self.state[-1, 0]

    def _update_padding_projective_plane(self):
        """Update the padding of a real projective plane board."""
        # Non-corner edges
        self._padded_state[0, 1:-1] = self.state[-1, ::-1]
        self._padded_state[-1, 1:-1] = self.state[0, ::-1]
        self._padded_state[1:-1, 0] = self.state[::-1, -1]
        self._padded_state[1:-1, -1] = self.state[::-1, 0]

        # Corners
        self._padded_state[0, 0] = self.state[0, 0]
        self._padded_state[0, -1] = self.state[0, -1]
        self._padded_state[-1, 0] = self.state[-1, 0]
        self._padded_state[-1, -1] = self.state[-1, -1]


def main(stdscr, *, geometry, prob, seed):
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
            curses.delay_output(60)
            life.evolve()
            c = stdscr.getch()
            if c != -1:
                break
        except KeyboardInterrupt:
            break


# Program description
_DESCRIPTION = "Conway's Game of Life."

# Available board geometries
_GEOMETRIES = [geometry.value for geometry in Geometry]

# Command line argument parsing
parser = argparse.ArgumentParser(description=_DESCRIPTION)

parser.add_argument("--geometry", choices=_GEOMETRIES, default="torus",
                    help="Specify the board geometry.")
parser.add_argument("--seed", type=int, default=None,
                    help="Pseudo-random number generator seed.")
parser.add_argument("--prob", type=float, default=0.25,
                    help="Probability of a cell starting out alive.")

if __name__ == "__main__":
    args = parser.parse_args()
    curses.wrapper(main, geometry=args.geometry, prob=args.prob, seed=args.seed)
