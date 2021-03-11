from . import parse_equations
import sys
import os
import shutil


def qed():
    """
    This is the entry point for the command-line script `qed`.

    """
    if len(sys.argv) == 1:
        parse_equations()
    elif len(sys.argv) == 2:
        parse_equations(os.path.dirname(os.path.abspath(sys.argv[1])))
    else:
        raise ValueError("Invalid option passed to `qed`.")


def qed_setup():
    """
    This is the entry point for the command-line script `qed-setup`.

    """
    # Create the temporary directory
    if not os.path.exists(".qed"):
        os.mkdir(".qed")

    # Copy the style file over
    if not os.path.exists("qed.sty"):
        shutil.copyfile(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "qed.sty"
            ),
            "qed.sty",
        )
