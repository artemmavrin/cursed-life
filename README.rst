Conway's Game of Life in Python 3.7
===================================

Play John Conway's
`Game of Life <https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life>`__ in the
terminal using the Python 3.7
`curses <https://docs.python.org/3.4/library/curses.html>`__ module.
The game board can be any of the following:

* A rectangle
* A cylinder
* A `torus <https://en.wikipedia.org/wiki/Torus>`__
* A `Möbius strip <https://en.wikipedia.org/wiki/Möbius_strip>`__
* A `Klein bottle <https://en.wikipedia.org/wiki/Klein_bottle>`__
* A `real projective plane <https://en.wikipedia.org/wiki/Real_projective_plane>`__


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
