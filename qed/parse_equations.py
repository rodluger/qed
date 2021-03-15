from .parse_latex_antlr import parse_latex
from .errors import LaTeXParsingError
import sympy
import glob
import os
from sympy.logic.boolalg import BooleanFalse, BooleanTrue


def parse_equation(equation):
    # TODO: We can do much better than this!
    try:
        value = sympy.simplify(parse_latex(equation)).doit()
    except LaTeXParsingError as e:
        return e
    if (type(value) is BooleanTrue) or (value is True):
        return True
    elif (type(value) is BooleanFalse) or (value is False):
        return False
    else:
        return None


def bool_to_icon(expr):
    if expr is True:
        return r"\testpassicon"
    elif expr is False:
        return r"\testfailicon"
    elif expr is None:
        return r"\testunknownicon"
    elif type(expr) is LaTeXParsingError:
        return r"\testerroricon"
    else:
        raise ValueError("Expression not understood.")


def parse_equations(path="."):
    files = glob.glob(os.path.join(path, ".qed_*.tex"))
    for file in files:
        with open(file, "r") as f:
            equation = f.read()
        with open(file.replace(".tex", ".icon"), "w") as f:
            result = parse_equation(equation)
            print(bool_to_icon(result), file=f)
