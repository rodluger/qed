from .constants import *
from .parse_custom import parse_custom_math
from .parse_latex_antlr import parse_latex
from .errors import LaTeXParsingError
from .math import Equivalence
import sympy
import glob
import os
from sympy.logic.boolalg import BooleanFalse, BooleanTrue
import warnings
from tqdm.auto import tqdm
import json
import numpy as np
from numpy.random import RandomState
from urllib.parse import urlencode
import re


def parse_equation_analytical(expr, options, output):
    try:
        value = sympy.simplify(sympy.simplify(expr).doit())
    except Exception as e:
        warnings.warn(str(e))
        output["ana"] = QEDERROR
        output["ams"] = str(e)
    else:
        if (type(value) is BooleanTrue) or (value is True):
            output["ana"] = QEDPASS
            output["ams"] = QEDMSGANATRUE
        elif (type(value) is BooleanFalse) or (value is False):
            output["ana"] = QEDFAIL
            output["ams"] = QEDMSGANAFALSE
        else:
            output["ana"] = QEDINDET
            output["ams"] = QEDMSGINDET
    return output


def parse_equation_numerical(expr, options, output):
    """
    TODO: Implement more granular reporting, with per-check statuses.
          Also report the actual value of the differences.

    """
    # Get the user options
    variables = options["variables"]
    atol = options["atol"]
    rtol = options["rtol"]
    seed = options["seed"]
    ntests = options["ntests"]
    low = options["low"]
    high = options["high"]

    # Determine variables automatically?
    if len(variables) == 0:
        rng = RandomState(seed)
        symbols = sorted(list(expr.free_symbols), key=lambda x: str(x))
        variables = []
        for k in range(ntests):
            dict_k = {}
            for symbol in symbols:
                dict_k[symbol] = rng.uniform(low=low, high=high)
            variables.append(dict_k)

    # Substitute and evaluate
    value = True
    if isinstance(expr, sympy.Equality):

        # Check the expression for every value of each of the variables
        for k in range(len(variables)):
            lhs = expr.lhs.subs(variables[k], simultaneous=True)
            rhs = expr.rhs.subs(variables[k], simultaneous=True)

            # Check the real and imaginary parts separately
            try:
                value = value and sympy.LessThan(
                    sympy.Abs(sympy.re(lhs - rhs)),
                    atol + rtol * sympy.Abs(sympy.re(rhs)),
                )
                value = value and sympy.LessThan(
                    sympy.Abs(sympy.im(lhs - rhs)),
                    atol + rtol * sympy.Abs(sympy.im(rhs)),
                )
            except Exception as e:
                # Fail fast
                warnings.warn(str(e))
                output["num"] = QEDERROR
                output["nms"] = str(e)
                return output
            else:
                if (type(value) is BooleanTrue) or (value is True):
                    # On to the next check
                    continue
                elif (type(value) is BooleanFalse) or (value is False):
                    # Fail fast
                    output["num"] = QEDFAIL
                    # TODO: More details
                    output["nms"] = QEDMSGNUMFALSE
                    return output
                else:
                    # This branch usually occurs when the user
                    # provided values for only *some* of the
                    # free variables. Let's re-run the
                    # evaluation with random values for the remaining
                    # variables.
                    new_options = options.copy()
                    new_options["variables"] = []
                    return parse_equation_numerical(expr, new_options, output)

        # All checks passed
        output["num"] = QEDPASS
        # TODO: More details
        output["nms"] = QEDMSGNUMTRUE
        return output

    else:

        # TODO! Implement inequalities
        warnings.warn("Branch not yet implemented.")
        output["num"] = QEDINDET
        output["nms"] = QEDMSGNOTIMP
        return output


def parse_equation(expr, options, variables, output):

    if isinstance(expr, Equivalence):

        # This is a definition. No tests to be performed.
        variables[expr.lhs] = expr.rhs
        output["ana"] = QEDNA
        output["num"] = QEDNA
        output["ams"] = QEDMSGDEF
        output["nms"] = QEDMSGDEF

    elif options["numerical"] == "yes":

        # Analytical evaluation disabled
        output["ana"] = QEDNA
        output["ams"] = QEDMSGANADIS
        output = parse_equation_numerical(expr, options, output)

    else:

        # Attempt analytical evaluation
        output = parse_equation_analytical(expr, options, output)
        if (output["ana"] != QEDPASS) and (options["numerical"] == "fallback"):
            # Fall back to numerical evaluation
            output = parse_equation_numerical(expr, options, output)
        else:
            output["num"] = QEDNA
            if output["ana"] == QEDPASS:
                output["nms"] = QEDMSGNONEED
            else:
                output["nms"] = QEDMSGNUMDIS

    return variables, output


def parse_options(options):
    # Cast settings appropriately
    options["timeout"] = float(options["timeout"])
    options["atol"] = float(options["atol"])
    options["rtol"] = float(options["rtol"])
    options["seed"] = int(options["seed"])
    options["ntests"] = int(options["ntests"])
    options["low"] = float(options["low"])
    options["high"] = float(options["high"])

    #
    assert options["numerical"] in [
        "yes",
        "no",
        "fallback",
    ], "Option `numerical` must be one of `yes`, `no`, or `fallback`."

    # Parse the variable values into substitution dicts
    sz = None
    for key, value in options["variables"].items():
        if type(value) is str:
            # Attempt to evaluate the expression
            value = eval(value)
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


def get_badge(output):
    # Get badge color
    if (output["ana"] == QEDPASS) or (output["num"] == QEDPASS):
        # Test passed
        color = "qedGreen"
        symbol = r"$\blacksquare$"
    elif (output["ana"] in [QEDFAIL, QEDERROR]) or (
        output["num"] in [QEDFAIL, QEDERROR]
    ):
        # Test failed or errored
        color = "qedRed"
        symbol = r"$\blacksquare$"
    elif (output["ana"] == QEDNA) and (output["num"] == QEDNA):
        # This is a definition
        color = "qedGreen"
        symbol = r"$\equiv$"
    else:
        # Indeterminate result
        color = "qedYellow"
        symbol = r"$\blacksquare$"

    # Get the url
    query_string = urlencode(output)
    url = "{}?{}".format(QEDWEBSITE, query_string)

    return r"\href{{{url}}}{{\color{{{color}}}{symbol}}}".format(
        color=color, url=url, symbol=symbol
    )


def parse_equations(path="."):
    texfiles = sorted(
        glob.glob(os.path.join(path, QEDQEDTEXFILES.format(qedCounter="*")))
    )
    custom_math = parse_custom_math(path=path)
    variables = {}
    print("[QED] Parsing equations...")
    for texfile in tqdm(texfiles):

        optfile = texfile.replace(".tex", ".json")
        iconfile = texfile.replace(".tex", ".icon")

        # Read the equation
        with open(texfile, "r") as f:
            equation = f.read()

        # Expand the function & symbol defs
        lat = str(equation)
        for function in custom_math["functions"].keys():
            latex_expr = custom_math["functions"][function][0]["latex"]
            if len(latex_expr):
                latex_expr = re.sub(
                    r"\\ensuremath\s+?\{(.*?)}", r"\1", latex_expr
                )
                latex_expr = latex_expr.replace(r"\protect", "")
                latex_expr = latex_expr.strip()
                lat = lat.replace(r"\{}".format(function), latex_expr)
        for symbol in custom_math["symbols"].keys():
            latex_expr = custom_math["symbols"][symbol]["latex"]
            if len(latex_expr):
                latex_expr = re.sub(
                    r"\\ensuremath\s+?\{(.*?)}", r"\1", latex_expr
                )
                latex_expr = latex_expr.replace(r"\protect", "")
                latex_expr = latex_expr.strip()
                lat = lat.replace(r"\{}".format(symbol), latex_expr)
        for key, val in QEDBUILTINS.items():
            lat = lat.replace(key, val)

        # Output dict
        output = {
            "eqn": int(os.path.basename(texfile)[:-4]),  # equation number
            "inp": equation.replace("=", "%3D"),  # raw latex input
            "lat": lat.replace("=", "%3D"),  # expanded latex input
        }

        # Read the options
        with open(optfile, "r") as f:
            options = json.load(f)
        options = parse_options(options)

        # Parse the LaTeX equation into a SymPy expression
        try:
            expr = parse_latex(equation, custom_math=custom_math)
        except LaTeXParsingError as e:
            warnings.warn(str(e))
            output["ana"] = QEDERROR
            output["ams"] = str(e)
            output["num"] = QEDNA
        else:
            output["sym"] = expr

            # Plug in global variables
            expr = expr.subs(variables)

            # Parse the SymPy expression into T/F
            variables, output = parse_equation(
                expr, options, variables, output
            )

        # Get the status badge
        badge = get_badge(output)

        # Export the badge
        with open(iconfile, "w") as f:
            print(badge, file=f)
