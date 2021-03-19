from .constants import QEDQEDTEXFILES
from .parse_custom import parse_custom_math
from .parse_latex_antlr import parse_latex
from .errors import LaTeXParsingError
import sympy
import glob
import os
from sympy.logic.boolalg import BooleanFalse, BooleanTrue
import warnings
from tqdm.auto import tqdm
import json
import numpy as np


class AnalyticalTrue(BooleanTrue):
    icon = r"\qedTestAnalyticalTrueIcon"


class AnalyticalFalse(BooleanFalse):
    icon = r"\qedTestAnalyticalFalseIcon"


class NumericalTrue(BooleanTrue):
    icon = r"\qedTestNumericalTrueIcon"


class NumericalFalse(BooleanFalse):
    icon = r"\qedTestNumericalFalseIcon"


class Indeterminate:
    icon = r"\qedTestIndeterminateIcon"


class ParsingError:
    icon = r"\qedTestParsingErrorIcon"


def parse_equation(equation, custom_math, options):

    # TODO: Log the outputs and errors

    # Parse the equation into a SymPy expression
    expr = parse_latex(equation, custom_math=custom_math)

    # Attempt to evaluate analytically
    if options["numerical"] != "true":
        try:
            value = sympy.simplify(sympy.simplify(expr).doit())
        except LaTeXParsingError as e:
            warnings.warn(str(e))
            return ParsingError

        # If we can determine T/F, return
        if (type(value) is BooleanTrue) or (value is True):
            return AnalyticalTrue()
        elif (type(value) is BooleanFalse) or (value is False):
            return AnalyticalFalse()
        else:
            pass

    # Attempt to evaluate numerically
    if options["numerical"] in ["true", "fallback"]:

        variables = options["variables"]
        atol = options["atol"]
        rtol = options["rtol"]
        value = True

        # TODO: Determine variables automatically?
        if len(variables) == 0:
            return Indeterminate()

        if isinstance(expr, sympy.Equality):

            # Check the expression for every value of each of the variables
            for k in range(len(variables)):
                lhs = expr.lhs.subs(variables[k], simultaneous=True)
                rhs = expr.rhs.subs(variables[k], simultaneous=True)
                value = value and sympy.LessThan(
                    sympy.Abs(lhs - rhs), atol + rtol * sympy.Abs(rhs)
                )
            if (type(value) is BooleanTrue) or (value is True):
                return NumericalTrue
            elif (type(value) is BooleanFalse) or (value is False):
                return NumericalFalse()
            else:
                return Indeterminate()

        else:

            # TODO: Process inequalities here
            return Indeterminate()

    else:

        return Indeterminate()


def to_icon(expr):
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


def parse_options(options):
    # TODO

    options["timeout"] = float(options["timeout"])
    options["atol"] = float(options["atol"])
    options["rtol"] = float(options["rtol"])

    # Parse the variable values into substitution dicts
    sz = None
    for key, value in options["variables"].items():
        value = np.atleast_1d(value)
        options["variables"][key] = value
        if sz is not None:
            assert len(value) == sz, "Mismatch in variable array sizes."
        sz = len(value)
    if sz is None:
        sz = 0
    variables = []
    for k in range(sz):
        dict_k = {}
        for key, value in options["variables"].items():
            dict_k[key] = value[k]
        variables.append(dict_k)
    options["variables"] = variables

    return options


def parse_equations(path="."):
    texfiles = glob.glob(
        os.path.join(path, QEDQEDTEXFILES.format(qedCounter="*"))
    )
    custom_math = parse_custom_math(path=path)
    print("[QED] Parsing equations...")
    for texfile in tqdm(texfiles):

        optfile = texfile.replace(".tex", ".json")
        iconfile = texfile.replace(".tex", ".icon")

        # Read the equation
        with open(texfile, "r") as f:
            equation = f.read()

        # Read the options
        with open(optfile, "r") as f:
            options = json.load(f)
        options = parse_options(options)

        # Parse the equation
        result = parse_equation(equation, custom_math, options)

        # Generate the pass/fail icon
        with open(iconfile, "w") as f:
            print(result.icon, file=f)
