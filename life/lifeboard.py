from life import GameOfLife

class LifeBoard(GameOfLife):
    '''Partial implementation of the Game of Life in a curses window.'''

    def __init__(self, scr, ch_alive, ch_dead, geometry=None):
        '''Initialize the class.

        Arguments:
            scr (curses.window):
                The window serving as the game board.
            ch_alive (char):
                The character representing a living cell.
            ch_dead (char):
                The character representing a dead cell.
        '''
        self.scr = scr
        self.ch_alive=ch_alive
        self.ch_dead=ch_dead
        # Get the dimensions of the board
        y, x = self.scr.getmaxyx()
        self.rows = y - 1  # I forgot why 1 is subtracted...
        self.cols = x
        # Create the underlying Game of Life board.
        super().__init__(self.rows, self.cols, geometry)
        # Populate the board randomly.
        self.random_board()

    def draw_cell(self, row, col, refresh=False):
        '''Draw a single cell of the board.

        Arguments:
            row (int):
                The row of the cell.
            col (int):
                The column of the cell.
            refresh (bool):
                If True, redraw the whole board.
                If False, wait to redraw.
        '''
        if self.state[row, col]:
            self.scr.addstr(row, col, self.ch_alive)
        else:
            self.scr.addstr(row, col, self.ch_dead)
        if refresh:
            self.scr.refresh()

    def toggle_cell(self, row, col):
        '''Change the state of the cell in the given row and column, and redraw
        the board.'''
        super().toggle_cell(row, col)
        self.draw_cell(row, col, refresh=True)

    def draw(self, update=True):
        '''Draw the current or next board state.

        Argument:
            update (bool):
                If True, draw the next generation.
                If False, draw the current generation.
        '''
        if update:
            self.update_board()
            self.draw(update=False)
        else:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.draw_cell(row, col)
            self.scr.refresh()
