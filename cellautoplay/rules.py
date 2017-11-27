import os
import sys
from random import choice, randint
from shutil import get_terminal_size
from time import sleep

import numpy
from numpy import zeros


term_width, term_height = get_terminal_size()


class Rule(object):

    def __init__(self, shape, generations, sleep_time, **kwargs):
        self.shape = shape  # (rows, cols) == (height, width)
        self.generations = generations
        self.sleep_time = sleep_time
        self.initial_grid = self.initialize_grid(self.make_grid(), **kwargs)

    def make_grid(self, shape=None):
        if shape is None:
            shape = self.shape
        return zeros(shape, dtype=self.cell_type)

    def get_moore_neighborhood(self, grid, coords, n=1):
        width = 1 + 2 * n
        neighborhood = self.make_grid((width, width))

        r, c = coords

        r_start = r - n
        r_end = r + n + 1
        c_start = c - n
        c_end = c + n + 1

        n_r_start = 0
        n_c_start = 0

        if r_start < 0:
            r_start = 0
            n_r_start = -r_start

        if c_start < 0:
            c_start = 0
            n_c_start = -c_start

        grid_slice = grid[r_start:r_end,c_start:c_end]
        h, w = grid_slice.shape
        n_r_end, n_c_end = n_r_start + h, n_c_start + w

        neighborhood[n_r_start:n_r_end,n_c_start:n_c_end] = grid_slice
        return neighborhood

    def get_empty_cells_in_neighborhood(self, neighborhood):
        empty_cells = []
        for r, row in enumerate(neighborhood):
            for c, val in enumerate(row):
                if not val:
                    empty_cells.append((r, c))
        return empty_cells

    def __iter__(self):
        grid = self.initial_grid
        height, width = grid.shape
        evolve = self.evolve
        make_grid = self.make_grid
        sleep_time = self.sleep_time
        sum = grid.sum()
        generation, generations = 0, self.generations
        while sum and generation < generations:
            yield grid
            sleep(sleep_time)
            new_grid = make_grid()
            for r in range(height):
                for c in range(width):
                    evolve(grid, new_grid, r, c)
            grid = new_grid
            sum = grid.sum()
            generation += 1


class Genesis(Rule):

    cell_type = numpy.int

    def initialize_grid(self, grid):
        height, width = grid.shape
        adam_row = randint(0, height - 1)
        adam_col = randint(0, width - 1)
        grid[adam_row,adam_col] = 18
        neighborhood = self.get_moore_neighborhood(grid, (adam_row, adam_col))
        val = True
        while val:
            eve_row = randint(0, neighborhood.shape[0] - 1)
            eve_col = randint(0, neighborhood.shape[1] - 1)
            val = neighborhood[eve_row,eve_col]
        neighborhood[eve_row,eve_col] = 18
        return grid

    def print_grid(self, grid, write=sys.stdout.writelines, flush=sys.stdout.flush):
        chars = ['\n']
        append = chars.append
        for row in grid:
            for c in row:
                if c == 0:
                    append(' ')
                elif c == 1:
                    append('B')
                elif c < 18:
                    append('C')
                elif c < 41:
                    append('M')
                elif c < 61:
                    append('A')
                else:
                    append('E')
            append('\n')
        write(chars)
        flush()

    def evolve(self, grid, new_grid, r, c):
        age = grid[r,c]
        neighborhood = self.get_moore_neighborhood(grid, (r, c), n=2)
        neighborhood_h, neighborhood_w = neighborhood.shape
        flat_neighborhood = neighborhood.flat

        if age:
            age += 1
            new_grid[r,c] = age

        if all((17 < a < 41) for a in flat_neighborhood):
            # If the neighborhood is all adults, *maybe* kill off 1 - 3 people.
            if choice([False]*99 + [True]):
                for i in range(randint(1, 3)):
                    kill_row = randint(0, neighborhood_h - 1)
                    kill_col = randint(0, neighborhood_w - 1)
                    neighborhood[kill_row,kill_col] = 0

        if not grid[r,c]:  # Current subject might have been killed off.
            age = 0

        if 17 < age < randint(36, 46):
            # If the current subject is a mating age adult, see if mating is
            # possible. There needs to be two or more adults and one open cell
            # in the neighborhood for birth to take place.
            mating_age_adults = [
                a for a in flat_neighborhood
                if 17 < a < randint(36, 46)
            ]
            num_mating_age_adults = len(mating_age_adults)
            if 1 < num_mating_age_adults < neighborhood.size:
                empty_cells = self.get_empty_cells_in_neighborhood(neighborhood)
                if empty_cells:
                    birth_cell = choice(empty_cells)
                    neighborhood[birth_cell] = 1
        elif age > randint(65, 100):
            # Die. This cell can now be reused for birth.
            age = 0

        new_grid[r,c] = age


class GameOfLife(Rule):

    cell_type = numpy.bool

    def initialize_grid(self, grid, initializer=None, **kwargs):
        if 'n' in kwargs:
            kwargs['n'] = int(kwargs['n'])
        if initializer:
            initializer = getattr(self, 'initializer_{0}'.format(initializer))
        else:
            initializer = lambda grid, r, c: randint(0, 1)
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                grid[r,c] = initializer(grid, r, c, **kwargs)
        return grid

    def initializer_all_cells(self, grid, r, c):
        return True

    def initializer_every_other_row(self, grid, r, c):
        return r % 2

    def initializer_first_n_cols(self, grid, r, c, n=2):
        return c < n

    def initializer_last_n_cols(self, grid, r, c, n=2):
        return self.shape[1] - c <= n

    def initializer_border(self, grid, r, c, n=2):
        return (
            (r < n) or
            (c < n) or
            (self.shape[0] - r <= n) or
            (self.shape[1] - c <= n)
        )

    def initializer_glider(self, grid, r, c):
        return (
            (r == 1 and c == 2) or
            (r == 2 and c == 3) or
            (r == 3 and c in (1, 2, 3))
        )

    def initializer_square(self, grid, r, c, n=(term_height // 2)):
        rows, cols = self.shape
        top = (cols - n) // 2
        bottom = top + n
        left = (rows - n) // 2
        right = left + n
        return (left < r < right) and (top < c < bottom)

    def initializer_x(self, grid, r, c):
        return c < r

    def get_grid_printer(self):
        rows, cols = self.shape

        # (False choice, True choice)
        # XXX: Seems to be slightly faster than a ternary.
        choices = (32, 42)

        lines = [b'\n']
        lines.extend(bytearray(cols + 1) for _ in range(rows))
        for line in lines[1:]:
            line[-1] = 10

        stdout = os.fdopen(sys.stdout.fileno(), 'wb')
        writelines = stdout.writelines
        flush = stdout.flush

        def print_grid(grid, lines=lines, choices=choices, writelines=writelines, flush=flush):
            for i, row in enumerate(grid, 1):
                line = lines[i]
                for j, is_on in enumerate(row):
                    line[j] = choices[is_on]
            writelines(lines)
            flush()

        return print_grid

    def evolve(self, grid, new_grid, r, c):
        val = grid[r,c]
        neighborhood = self.get_moore_neighborhood(grid, (r, c), n=1)
        num_alive = neighborhood.sum()
        if num_alive == 3:
            new_val = 1
        elif num_alive == 4:
            new_val = val
        else:
            new_val = 0
        new_grid[r,c] = new_val


elementary_rules = {}
elementary_rules[110] = {
    (1, 1, 1): 0,
    (1, 1, 0): 1,
    (1, 0, 1): 1,
    (1, 0, 0): 0,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0,
}
elementary_rules[30] = {
    (1, 1, 1): 0,
    (1, 1, 0): 0,
    (1, 0, 1): 0,
    (1, 0, 0): 1,
    (0, 1, 1): 1,
    (0, 1, 0): 1,
    (0, 0, 1): 1,
    (0, 0, 0): 0,
}
