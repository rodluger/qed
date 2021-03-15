from . import parse_equations
import sys
import os
import shutil
import glob


def qed():
    """
    This is the entry point for the command-line script `qed`.

    """
    assert len(sys.argv) == 1, "Invalid option."
    parse_equations()


def qed_setup():
    """
    This is the entry point for the command-line script `qed-setup`.

    """
    assert len(sys.argv) == 1, "Invalid option."
    shutil.copyfile(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "qed.sty"),
        "qed.sty",
    )


def qed_clean():
    """
    This is the entry point for the command-line script `qed-clean`.

    """
    assert len(sys.argv) == 1, "Invalid option."
    for file in glob.glob(".qed_*"):
        os.remove(file)
