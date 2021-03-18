import os

try:
    from .qed_version import __version__
except ModuleNotFoundError:
    __version__ = "unknown"

if not os.getenv("QED_BUILD_LATEX_ANTLR", False):

    from .errors import LaTeXParsingError
    from .parse_latex_antlr import parse_latex
    from .parse_equations import parse_equation, parse_equations
    from . import entry_points
