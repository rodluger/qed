from .constants import QEDFILEPATH
from .parse_custom import parse_custom_math
from .parse_latex_antlr import parse_latex
from .errors import LaTeXParsingError
import sympy
import glob
import os
from sympy.logic.boolalg import BooleanFalse, BooleanTrue
import warnings


def parse_equation(equation, custom_math):
    # TODO: We can do much better than this!
    try:
        value = sympy.simplify(
            sympy.simplify(
                parse_latex(equation, custom_math=custom_math)
            ).doit()
        )
    except LaTeXParsingError as e:
        # TODO: Log the error
        warnings.warn(str(e))
        return e
    if (type(value) is BooleanTrue) or (value is True):
        return True
    elif (type(value) is BooleanFalse) or (value is False):
        return False
    else:
        # TODO: Log this
        return None


def bool_to_icon(expr):
    if expr is True:
        return r"\qedTestPassIcon"
    elif expr is False:
        return r"\qedTestFailIcon"
    elif expr is None:
        return r"\qedTestUnknownIcon"
    elif type(expr) is LaTeXParsingError:
        return r"\qedTestErrorIcon"
    else:
        raise ValueError("Expression not understood.")


def parse_equations(path="."):
    files = glob.glob(os.path.join(path, QEDFILEPATH, "*.tex"))
    custom_math = parse_custom_math(path=path)
    for file in files:
        with open(file, "r") as f:
            equation = f.read()
        with open(file.replace(".tex", ".icon"), "w") as f:
            result = parse_equation(equation, custom_math)
            print(bool_to_icon(result), file=f)
