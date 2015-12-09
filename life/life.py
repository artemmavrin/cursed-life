from itertools import cycle, product
import numpy as np


RECTANGLE = 0
CYLINDER = 1
MOBIUS = 2
TORUS = 3
KLEIN = 4
RP2 = 5
GEOMETRIES = (RECTANGLE, CYLINDER, MOBIUS, TORUS, KLEIN, RP2)
GEOMETRY_NAME = {
    RECTANGLE: 'Rectangle',
    CYLINDER: 'Cylinder',
    MOBIUS: 'Möbius Strip',
    TORUS: 'Torus',
    KLEIN: 'Klein Bottle',
    RP2: 'Real Projective Plane'
    }

class GameOfLife(object):
    '''General class to run Conway's zero-player Game of Life.
    The game board is a 2D Numpy array of boolean values. True represents a
    living cell, False represents a dead cell.
    The game board can be a bounded rectangle, a torus, or a Klein bottle.
    '''

    def __init__(self, rows, cols, geometry=None):
        '''Initialize the class, creating an empty board.

        Arguments:
            rows (int):
                The number of rows of the board.
            cols (int):
                The number of columns of the board.
            geometry (str):
                The geometry of the board.
                'rectangle', 'torus', or 'klein'.
        '''
        # Create repreating sequence of possible geometries
        self.geometries = cycle(GEOMETRIES)
        self.rows = rows
        self.cols = cols
        self.toggle_geometry(geometry)
        self.clear()

    def clear(self):
        '''Clear the board of all living cells.'''
        self.state = np.array([[False] * self.cols] * self.rows)

    def random_board(self):
        '''Create a random board state.'''
        self.state = np.random.choice([True, False], [self.rows, self.cols])

    def toggle_geometry(self, geometry=None):
        '''Toggle the geometry of the board.'''
        if geometry is None:
            self.geometry = next(self.geometries)
        elif geometry in GEOMETRIES:
            self.geometry = geometry
            # Set geometries cycle to the correct position
            while next(self.geometries) != geometry:
                pass
        else:
            raise ValueError('Invalid geometry: ' + str(geometry))

    def toggle_cell(self, row, col):
        '''Toggle the status (alive or dead) of a cell.'''
        self.state[row, col] = not self.state[row, col]

    def neighbors(self, row, col):
        '''Yield the coordinates of the neighbors of the given cell.'''
        # Orientable geometries.
        # x and y coordinates do not depend on each other.
        if self.geometry == RECTANGLE:
            ys = range(max(0, row - 1), min(self.rows, row + 2))
            xs = range(max(0, col - 1), min(self.cols, col + 2))
            for y, x in product(ys, xs):
                 if (y, x) != (row, col):
                     yield y, x
        elif self.geometry == CYLINDER:
            ys = range(max(0, row - 1), min(self.rows, row + 2))
            xs = ((col + j) % self.cols for j in range(-1, 2))
            for y, x in product(ys, xs):
                 if (y, x) != (row, col):
                     yield y, x
        elif self.geometry == TORUS:
            ys = ((row + i) % self.rows for i in range(-1, 2))
            xs = ((col + j) % self.cols for j in range(-1, 2))
            for y, x in product(ys, xs):
                 if (y, x) != (row, col):
                     yield y, x
        # Non-orientable geometries are a bit more complicated.
        # x and y coordinates can depend on each other.
        elif self.geometry == MOBIUS:
            ys = range(max(0, row - 1), min(self.rows, row + 2))
            for y, j in product(ys, range(-1, 2)):
                x = (col + j) % self.cols
                if (col, j) in ((0, -1), (self.cols - 1, 1)):
                    y = self.rows - 1 - y
                if (y, x) != (row, col):
                    yield y, x
        elif self.geometry == KLEIN:
            for i, j in product(range(-1, 2), range(-1, 2)):
                y = (row + i) % self.rows
                x = (col + j) % self.cols
                if (col, j) in ((0, -1), (self.cols - 1, 1)):
                    y = self.rows - 1 - y
                if (y, x) != (row, col):
                    yield y, x
        elif self.geometry == RP2:
            for i, j in product(range(-1, 2), range(-1, 2)):
                y = (row + i) % self.rows
                x = (col + j) % self.cols
                if (col, j) in ((0, -1), (self.cols - 1, 1)):
                    y = self.rows - 1 - y
                if (row, i) in ((0, -1), (self.rows - 1, 1)):
                    x = self.cols - 1 - x
                if (y, x) != (row, col):
                    yield y, x

    def num_neighbors(self, row, col):
        '''Return the number of living neighbors of the given cell.'''
        return sum(1 for y, x in self.neighbors(row, col) if self.state[y, x])

    def update_board(self):
        '''Create the next generation of the board.'''
        next_state = np.array([[False] * self.cols] * self.rows)
        for row in range(self.rows):
            for col in range(self.cols):
                neighbors = self.num_neighbors(row, col)
                if self.state[row, col]:
                    # The cell is alive
                    if neighbors in (2, 3):
                        next_state[row, col] = True
                else:
                    # The cell is dead
                    if neighbors == 3:
                        next_state[row, col] = True
        self.state = next_state
