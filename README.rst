Cellular Automata Playground
++++++++++++++++++++++++++++

Intro
=====

I threw this together so I could play around with the Game of Life and related
stuff. It's not particularly sophisticated, but it's fun and the output can be
mesmerizing.

Installation
============

Targets Python 3; Python 2.7 should work too.

NumPy is the only dependency. If you're running Linux, you probably won't need
to do anything special; just ``pip install`` the package and you should be good
to go. For other platforms, you might need to install a binary package before
running ``pip install``; those can be found here: http://scipy.org/Download.

Note: Installation isn't strictly necessary. You can just install NumPy into
your site-packages and then run the script like so (assuming $PWD is the top
level of the project)::

    python -m cellautoplay ...

Buildout
--------

If you're into Buildout (as I am), you can use the supplied buildout.cfg and
simply run `buildout` in the project directory. This will generate the cellauto
script in ./bin.

Running
=======

If you ``pip install`` the package, there will be a console script you can
run::

    $ cellauto -h

If you install via Buildout, the script will be in ./bin::

    $ ./bin/cellauto -h

If you don't want to install the package, you can run the script like this::

    $ python -m cellautoplay -h

For the best experience, put your terminal into full screen mode and figure out
the number of rows and columns it has.

Game of Life
------------

Okay, here's how to actually run the script::

    $ cellauto --rule GameOfLife -r 62 -c 211

In this example, the grid will be randomly initialized. It's also possible to
intialize the grid in a deterministic way::

    $ cellauto --rule GameOfLife -r 62 -c 211 initializer=all_cells

Initializing all rows doesn't do anything interesting. Try this instead::

    $ cellauto --rule GameOfLife -r 62 -c 211 initializer=border n=2

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

Genesis is always initialized in a random fashion::

    $ cellauto --rule Genesis -r 62 -c 211 