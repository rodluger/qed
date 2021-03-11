from .parse_latex_antlr import parse_latex
import sympy
import glob
import os
from sympy.logic.boolalg import BooleanFalse, BooleanTrue


def parse_equation(equation):
    # TODO: We can do much better than this!
    value = sympy.simplify(parse_latex(equation)).doit()
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
    else:
        return r"\testunknownicon"


def parse_equations(path="."):
    files = glob.glob(os.path.join(path, ".qed", "*.tex"))
    for file in files:
        with open(file, "r") as f:
            equation = f.read()
        with open(file.replace(".tex", ".icon"), "w") as f:
            print(bool_to_icon(parse_equation(equation)), file=f)
