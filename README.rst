Conway's Game of Life in Python 3.7
===================================

Play John Conway's
`Game of Life <https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life>`__ in the
terminal using the Python 3.7
`curses <https://docs.python.org/3/library/curses.html>`__ module.
The Game of Life is a cellular automaton consisting of discrete "cells" living
on a compact board. Each cell is either "alive" or "dead" at a given moment. At
discrete time steps, a cell's state evolves according to the following rules:

* If a cell is alive, then it remains alive in the next generation if it has two
  or three living neighbors; otherwise, it dies.
* If a cell is dead, then it becomes alive in the next generation if it has
  three living neighbors; otherwise, it remains dead.

Traditionally, the Game of Life is played on a rectangular board where cells
along the edges have a limited neighborhood. In our version, the game board can
be any of the following compact surfaces:

* A rectangle
* A cylinder
* A `torus <https://en.wikipedia.org/wiki/Torus>`__
* A `Möbius strip <https://en.wikipedia.org/wiki/Möbius_strip>`__
* A `Klein bottle <https://en.wikipedia.org/wiki/Klein_bottle>`__
* A `real projective plane <https://en.wikipedia.org/wiki/Real_projective_plane>`__

All of these non-rectangle boards can be visualized as a rectangle with one or
more pairs of edges identified.

.. figure:: images/glider_rp2.gif
    :alt: glider on a real projective plane

    **Figure.** A
    `glider <https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)>`__ moving
    on a real projective plane.

Installation
------------

.. code:: shell

    git clone https://github.com/artemmavrin/cursed-life.git
    cd cursed-life
    python -m pip install -r requirements.txt
    python setup.py install


Usage
-----

.. code:: shell

    python -m life

To see usage instructions and additional command-line arguments, run

.. code:: shell

    python -m life --help
