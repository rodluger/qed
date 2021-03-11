from . import parse_equations
import sys
import os


def entry_point():
    """
    This is the entry point for the command-line script `starry-process`.
    We set up a server and launch the page below.

    """
    if len(sys.argv) == 1:
        parse_equations()
    elif len(sys.argv) == 2:
        parse_equations(os.path.dirname(os.path.abspath(sys.argv[1])))
    else:
        raise ValueError("Invalid option passed to `qed`.")
