Cellular Automata Playground
++++++++++++++++++++++++++++

Intro
=====

I threw this together so I could play around with the Game of Life and related
stuff. It's not particularly sophisticated, but it's fun and the output can be
mesmerizing.

Installation
============

- Requires Python 3.7+
- Uses poetry for dependency/package management
- NumPy is the only dependency
- `poetry install`

Running
=======

After you install the package, there will be a console script you can run::

    $ cellauto -h

Game of Life
------------

::

    $ cellauto --rule GameOfLife

In this example, the grid will be randomly initialized. It's also possible to
intialize the grid in a deterministic way::

    $ cellauto --rule GameOfLife initializer=all_cells

Initializing all cells doesn't do anything interesting. Try this instead::

    $ cellauto --rule GameOfLife initializer=border n=2

There are other intializers available; see `rules.GameOfLife` to see what they
are. You can also write your own. Just add a method whose name starts with
`initializer_` that takes the grid, a row, and a column as args and returns
True if the cell should be on initially or False if it should be off. If your
initializer has keyword args, these can be set via the command line as shown
above (`n=2`).

Genesis
-------

There's another game included called Genesis. It starts out with a population
of two adults and then evolves from there according to various rules (natural
death, random death due to overpopulation, and birth).

Genesis is always initialized randomly::

    $ cellauto --rule Genesis
