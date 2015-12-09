import curses

from life import *
from lifeboard import LifeBoard

def main(stdscr):
    '''Run the program in the terminal. This function will be wrapped in
    curses.wrapper() to safely enter and exit the program.
    '''
    # Begin by clearing the screen.
    stdscr.clear()

    # Get the dimensions of the terminal.
    rows, cols = stdscr.getmaxyx()

    # Define the subwindows of the terminal.
    menu_window = stdscr.subwin(1, cols, 0, 0)
    board_window = stdscr.subwin(rows - 4, cols - 2, 2, 1)
    border_window = stdscr.subwin(rows - 2, cols, 1, 0)
    geometry_window = stdscr.subwin(1, cols, rows - 2, 0)
    message_window = stdscr.subwin(1, cols, rows - 1, 0)

    def clear_message():
        '''Clear the text in the message window.'''
        message_window.move(0, 0)
        message_window.clrtoeol()
        message_window.refresh()

    def set_message(line):
        '''Display a message in the message window.'''
        message_window.addstr(0, 0, line)
        message_window.refresh()

    def clear_menu():
        '''Clear the text in the menu window.'''
        menu_window.move(0, 0)
        menu_window.clrtoeol()
        menu_window.refresh()

    def set_menu(line):
        '''Display the menu.'''
        menu_window.addstr(0, 0, line)
        menu_window.refresh()

    def display_geometry(editable=True):
        '''Display the current board geometry.'''
        geometry_window.move(0,0)
        geometry_window.clrtoeol()
        geometry_window.addstr(0, 0, '(G)eometry: ')
        geometry_window.addstr(GEOMETRY_NAME[board.geometry])
        geometry_window.refresh()

    def draw_border():
        '''Change the border to reflect the fundamental polygon of the current
        geometry.'''
        corner = '+'
        if board.geometry == RECTANGLE:
            top = bottom = '-'
            left = right = '|'
        elif board.geometry == CYLINDER:
            top = bottom = '-'
            left = right = 'v'
        elif board.geometry == MOBIUS:
            top = bottom = '-'
            left = '^'
            right = 'v'
        elif board.geometry == TORUS:
            top = bottom = '>'
            left = right = 'v'
        elif board.geometry == KLEIN:
            top = bottom = '>'
            left = '^'
            right = 'v'
        elif board.geometry == RP2:
            top = '>'
            bottom = '<'
            left = '^'
            right = 'v'
        # Draw the corners of the board.
        border_window.addstr(0, 0, corner)
        border_window.addstr(0, cols - 1, corner)
        border_window.addstr(rows - 4, 0, corner)
        border_window.addstr(rows - 4, cols - 1, corner)
        # Draw the top and bottom
        border_window.addstr(0, 1, top * (cols - 2))
        border_window.addstr(rows - 4, 1, bottom * (cols - 2))
        # Draw the sides
        for row in range(rows - 5):
            border_window.addstr(row + 1, 0, left)
            border_window.addstr(row + 1, cols - 1, right)
        border_window.refresh()
        geometry_window.refresh()


    # These are the messages/menus that will show up in the message/menu window.
    message = 'Use the arrow keys to move the cursor. '
    message += 'Press <Enter> to toggle a cell.'
    menu_pause = '<Space> Play, (R)andom, (C)lear, (A)dvance, (Q)uit'
    menu_play = '<Space> Pause, (R)andom, (C)lear, (Q)uit'

    # Initialize the Game of Life board (randomly).
    board = LifeBoard(board_window, '*', ' ', TORUS)

    # Draw everything on the screen
    board.draw(update=False)
    display_geometry()
    draw_border()
    set_message(message)
    set_menu(menu_pause)

    # Make the cursor extra visible and put it in the center of the board.
    curses.curs_set(2)
    cursor_y = board.rows // 2 + 1
    cursor_x = board.cols // 2
    stdscr.move(cursor_y, cursor_x)

    # Main loop starts now.
    running = False
    while True:
        if running:
            # Small delay to give the terminal time to print everything.
            curses.delay_output(50)
            # Draw the next generation of the board.
            board.draw()
        # Wait for input from the user.
        c = stdscr.getch()
        if 0 <= c < 256:
            # c is ASCII.
            c = chr(c)
            if c == ' ':
                if not running:
                    # Start running the game continuously.
                    running = True
                    # First, hide the cursor.
                    curses.curs_set(0)
                    # Don't wait for the user to enter anything.
                    stdscr.timeout(0)
                    # Clear the message window
                    clear_message()
                    # Display the play menu
                    clear_menu()
                    set_menu(menu_play)
                else:
                    # Stop running continuously.
                    running = False
                    # Begin waiting for user input again.
                    stdscr.timeout(-1)
                    # Unhide the cursor.
                    curses.curs_set(2)
                    # Display the message window
                    set_message(message)
                    # Display the pause menu
                    clear_menu()
                    set_menu(menu_pause)
            elif c in 'qQ':
                # Exit the main loop, and hence the program.
                break
            elif c in 'cC':
                # Clear the screen (kill all living cells on the board).
                board.clear()
                board.draw(update=False)
            elif c in 'rR':
                # Create a new randomly populated board.
                board.random_board()
                board.draw(update=False)
            elif c in 'gG':
                # Change the board geometry.
                board.toggle_geometry()
                display_geometry()
                draw_border()
            elif c in 'aA':
                # Advance the board by one generation.
                if not running:
                    board.draw()
            elif c == '\n':
                # Toggle the state of the cell where the cursor is positioned.
                if not running:
                    board.toggle_cell(cursor_y - 2, cursor_x - 1)
        # Now look for key presses if the game is not running.
        if not running:
            if c == curses.KEY_UP:
                # Move the cursor up if possible.
                if cursor_y > 2:
                    cursor_y -= 1
                else:
                    if board.geometry in (RECTANGLE, CYLINDER, MOBIUS):
                        curses.flash()
                    elif board.geometry in (TORUS, KLEIN):
                        cursor_y = board.rows + 1
                    elif board.geometry == RP2:
                        cursor_y = board.rows + 1
                        cursor_x = board.cols - cursor_x + 1
            elif c == curses.KEY_DOWN:
                # Move the cursor down if possible.
                if cursor_y < board.rows + 1:
                    cursor_y += 1
                else:
                    if board.geometry in (RECTANGLE, CYLINDER, MOBIUS):
                        curses.flash()
                    elif board.geometry in (TORUS, KLEIN):
                        cursor_y = 2
                    elif board.geometry == RP2:
                        cursor_y = 2
                        cursor_x = board.cols - cursor_x + 1
            elif c == curses.KEY_LEFT:
                # Move the cursor left if possible.
                if cursor_x > 1:
                    cursor_x -= 1
                else:
                    if board.geometry == RECTANGLE:
                        curses.flash()
                    elif board.geometry in (CYLINDER, TORUS):
                        cursor_x = board.cols
                    elif board.geometry in (MOBIUS, KLEIN, RP2):
                        cursor_x = board.cols
                        cursor_y = board.rows - cursor_y + 3
            elif c == curses.KEY_RIGHT:
                # Move the cursor right if possible.
                if cursor_x < board.cols:
                    cursor_x += 1
                else:
                    if board.geometry == RECTANGLE:
                        curses.flash()
                    elif board.geometry in (CYLINDER, TORUS):
                        cursor_x = 1
                    elif board.geometry in (MOBIUS, KLEIN, RP2):
                        cursor_x = 1
                        cursor_y = board.rows - cursor_y + 3
            elif c == curses.KEY_MOUSE:
                # If a mouse was clicked, position the cursor at the clicked cell.
                # Note to self: on Mac OS X, do ALT-CLICK to click.
                _, x, y, _, bstate = curses.getmouse()
                if bstate == curses.BUTTONn_CLICKED:
                    cursor_x = x
                    cursor_y = y
            # Finally, move the cursor to potentially new location.
            stdscr.move(cursor_y, cursor_x)


# Run the program!
curses.wrapper(main)
