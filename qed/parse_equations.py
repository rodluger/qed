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
import itertools


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


def parse_equation_numerical(expr, options, variables, output):
    """

    """
    # Get the user options
    atol = options["atol"]
    rtol = options["rtol"]
    seed = options["seed"]

    # All the free symbols in the expression
    symbols = sorted([str(symbol) for symbol in expr.free_symbols])

    #
    ntests = options["ntests"]
    rng = RandomState(seed)
    subs = [{} for n in range(ntests)]
    for symbol in symbols:
        for n in range(ntests):
            sgn = -1 if np.random.random() < 0.5 else 1
            subs[n][symbol] = sgn * 10 ** (rng.uniform(low=-5, high=5))

    # Substitute and evaluate
    results = [{} for n in range(ntests)]
    if isinstance(expr, sympy.Equality):

        # Check the expression for every value of each of the variables
        for n in range(ntests):

            try:

                # Plug in values
                lhs = expr.lhs.subs(subs[n], simultaneous=True)
                rhs = expr.rhs.subs(subs[n], simultaneous=True)

                # Check the real and imaginary parts separately
                lhs_re = float(sympy.re(lhs).evalf())
                lhs_im = float(sympy.im(lhs).evalf())
                rhs_re = float(sympy.re(rhs).evalf())
                rhs_im = float(sympy.im(rhs).evalf())
                diff_re = np.abs(lhs_re - rhs_re)
                diff_im = np.abs(lhs_im - rhs_im)

                # Maximum allowed difference (same as in `np.allclose`)
                maxdiff_re = atol + rtol * np.abs(rhs_re)
                maxdiff_im = atol + rtol * np.abs(rhs_im)

                # Check it
                passed = (diff_re <= maxdiff_re) and (diff_im <= maxdiff_im)
                results[n] = {
                    "passed": int(passed),
                    "variables": subs[n],
                    "diff_re": diff_re,
                    "diff_im": diff_im,
                    "maxdiff_re": maxdiff_re,
                    "maxdiff_im": maxdiff_im,
                }

            except Exception as e:
                # Fail fast
                warnings.warn(str(e))
                output["num"] = QEDERROR
                output["nms"] = str(e)
                return output

        # Pass/fail?
        if np.all([result["passed"] for result in results]):
            output["num"] = QEDPASS
            output["nms"] = QEDMSGNUMTRUE
        else:
            output["num"] = QEDFAIL
            output["nms"] = QEDMSGNUMFALSE

        # Save the info from each test
        for n in range(ntests):
            output[
                "n{:02d}".format(n)
            ] = "{passed:1d},{diff_re:.3e},{diff_im:.3e},{maxdiff_re:.3e},{maxdiff_im:.3e}".format(
                **results[n]
            )
            for k, variable in enumerate(results[n]["variables"].keys()):
                output["v{:02d}{:02d}".format(n, k)] = "{:s},{:.3e}".format(
                    variable, results[n]["variables"][variable]
                )

        return output

    else:

        # TODO! Implement inequalities
        warnings.warn("Branch not yet implemented.")
        output["num"] = QEDINDET
        output["nms"] = QEDMSGNOTIMP
        return output


def parse_equation(expr, options, variables, output):

    # Attempt analytical evaluation
    output = parse_equation_analytical(expr, options, output)

    if output["ana"] == QEDPASS:

        # No need to evaluate things numerically
        output["num"] = QEDNA
        output["nms"] = QEDMSGNONEED

    else:

        # Fall back to numerical evaluation
        output = parse_equation_numerical(expr, options, variables, output)

    return output


def parse_options(options):
    # Cast settings appropriately
    options["timeout"] = float(options["timeout"])
    options["atol"] = float(options["atol"])
    options["rtol"] = float(options["rtol"])
    options["seed"] = int(options["seed"])
    options["ntests"] = int(options["ntests"])
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
    subs = {}
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

            # Plug in global substitutions
            expr = expr.subs(subs)

            if isinstance(expr, Equivalence):

                # This is a definition. No tests to be performed.
                subs[expr.lhs] = expr.rhs
                output["ana"] = QEDNA
                output["num"] = QEDNA
                output["ams"] = QEDMSGDEF
                output["nms"] = QEDMSGDEF

            else:

                # Parse the SymPy expression into T/F
                output = parse_equation(expr, options, variables, output)

        # Get the status badge
        badge = get_badge(output)

        # Export the badge
        with open(iconfile, "w") as f:
            print(badge, file=f)
