import argparse
import pickle
import sys
from shutil import get_terminal_size

from cellautoplay import rules


def main(argv=None):
    term_size = get_terminal_size()
    default_rows = term_size.lines - 3
    default_columns = term_size.columns - 2

    parser = argparse.ArgumentParser()
    parser.add_argument('--rule', '-R', required=True)
    parser.add_argument('--rows', '-r', type=int, default=default_rows)
    parser.add_argument('--cols', '-c', type=int, default=default_columns)
    parser.add_argument('--generations', '-g', type=int, default=20*(2**30))
    parser.add_argument('--sleep-time', '-t', type=float, default=.1)
    parser.add_argument('kwargs', nargs='*')

    if argv:
        args = parser.parse_args(argv)
    else:
        args = parser.parse_args()

    RuleType = getattr(rules, args.rule)

    if args.kwargs:
        kwargs = dict(item.split('=') for item in args.kwargs)
    else:
        kwargs = {}

    rule = RuleType(
        (args.rows, args.cols), args.generations, args.sleep_time, **kwargs)

    print_grid = rule.print_grid

    # Save grid in case it produces super cool results
    with open('cellular_automaton_grid.pickle', 'wb') as fp:
        pickle.dump(rule.initial_grid, fp)

    for generation in rule:
        print_grid(generation)

    print('\n' * args.rows)
    print('Game over.')
    return 1


if __name__ == '__main__':
    sys.exit(main())
