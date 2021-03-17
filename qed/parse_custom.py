from .constants import QEDFUNCTIONFILE, QEDSYMBOLFILE, QEDSEPARATORS
import re
import os
import sympy

__all__ = ["parse_custom_math"]


def parse_custom_functions(path="."):

    func_dict = {}

    # If no funcs were defined, return empty
    if not os.path.exists(os.path.join(path, QEDFUNCTIONFILE)):
        return func_dict

    # Open the auto-generated functions file
    with open(os.path.join(path, QEDFUNCTIONFILE), "r") as f:
        functions = f.readlines()

    # Build the custom function dictionary
    for function in functions:

        # Parse the properties
        match = re.match("\{(.*?)\}" * 5, function)
        if match:
            name, desc, args, latex, sympy_code = match.groups()
        else:
            raise ValueError("Cannot parse function properties.")

        # Parse the function arguments
        arguments = str(args)
        for sep in QEDSEPARATORS:
            arguments = arguments.replace(sep, ",")
        arguments = arguments.split(",")
        arguments = [arg.strip() for arg in arguments]

        # Parse the argument separators
        if len(arguments) > 1:
            pattern = r"\s*([{}])\s*".format(
                re.escape("".join(QEDSEPARATORS))
            ).join([re.escape(arg) for arg in arguments])
            match = re.match(pattern, args)
            if match:
                separators = match.groups()
            else:
                raise ValueError(
                    "Cannot parse the arguments of function `{}`.".format(name)
                )
        else:
            separators = []

        # Parse the sympy code
        sympy_code = eval(sympy_code)

        # Basic checks
        assert (
            len(arguments) > 0
        ), "Function `{}` must have at least one argument.".format(name)
        assert callable(
            sympy_code
        ), "Property `sympy` of function `{}` must be a callable.".format(name)

        # Populate the dictionary
        props = {
            "description": desc,
            "arguments": arguments,
            "separators": separators,
            "latex": latex,
            "sympy": sympy_code,
        }
        if name in func_dict.keys():
            func_dict[name] += [props]
        else:
            func_dict[name] = [props]

    return func_dict


def parse_custom_symbols(path="."):

    sym_dict = {}

    # If no symbols were defined, return empty
    if not os.path.exists(os.path.join(path, QEDSYMBOLFILE)):
        return sym_dict

    # Open the auto-generated symbols file
    with open(os.path.join(path, QEDSYMBOLFILE), "r") as f:
        symbols = f.readlines()

    # Build the custom symbol dictionary
    for symbol in symbols:

        # Parse the properties
        match = re.match("\{(.*?)\}" * 4, symbol)
        if match:
            name, desc, latex, sympy_code = match.groups()
        else:
            raise ValueError("Cannot parse symbol properties.")

        # Parse the sympy code
        sympy_code = eval(sympy_code)

        # Populate the dictionary
        props = {"description": desc, "latex": latex, "sympy": sympy_code}
        if name in sym_dict.keys():
            raise ValueError(
                "Multiple definitions for symbol `{}`.".format(name)
            )
        else:
            sym_dict[name] = props

    return sym_dict


def parse_custom_math(path="."):
    custom_math = {
        "functions": parse_custom_functions(path),
        "symbols": parse_custom_symbols(path),
    }
    return custom_math
