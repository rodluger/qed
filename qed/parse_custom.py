from .custom import CUSTOM_MATH
import sympy


__all__ = ["get_custom_math"]


FUNCTION_TEMPLATE = {
    "description": "User-defined function",
    "arguments": [],
    "separators": [],
    "latex": None,
    "sympy": lambda *args: sympy.Integer(0),
}

SEPARATORS = [",", ";", "|"]

SYMBOL_TEMPLATE = {
    "description": "User-defined symbol",
    "latex": None,
    "sympy": lambda *args: sympy.Integer(0),
}


def process_custom(custom):
    """
    Check the syntax of custom definitions and
    rectify entries if possible.

    """
    # Make a copy
    new_custom = custom.copy()
    new_custom["functions"] = new_custom.get("functions", {})
    new_custom["symbols"] = new_custom.get("symbols", {})

    # Process function definitions
    for key in custom.get("functions", {}).keys():

        # Ensure function definitions are lists
        if not isinstance(new_custom["functions"][key], list):
            new_custom["functions"][key] = [new_custom["functions"][key]]

        # Process each definition
        entries = [
            FUNCTION_TEMPLATE.copy() for entry in new_custom["functions"][key]
        ]
        for i, entry in enumerate(entries):

            # Ensure it's a dict
            assert isinstance(
                entry, dict
            ), "Function definition `{}` must be a dictionary.".format(key)

            # Update with defaults
            entry.update(new_custom["functions"][key][i])
            new_custom["functions"][key][i] = entry

            # Basic checks
            args = new_custom["functions"][key][i]["arguments"]
            seps = new_custom["functions"][key][i]["separators"]
            latex_ = new_custom["functions"][key][i]["latex"]
            sympy_ = new_custom["functions"][key][i]["sympy"]
            assert isinstance(
                args, list
            ), "Property `arguments` of function `{}` must be a list.".format(
                key
            )
            assert (
                len(args) > 0
            ), "Function `{}` must have at least one argument.".format(key)
            assert isinstance(
                seps, list
            ), "Property `separators` of function `{}` must be a list."
            assert (
                len(args) == len(seps) + 1
            ), "Function `{}` has the wrong number of argument separators.".format(
                key
            )
            for arg in args:
                assert isinstance(
                    arg, str
                ), "Arguments to function `{}` must be strings.".format(key)
            for sep in seps:
                assert (
                    sep in SEPARATORS
                ), "Separators for function `{}` must be one of {}.".format(
                    key, SEPARATORS
                )
            assert latex_ is None or isinstance(
                latex_, str
            ), "Property `latex` of function `{}` must be a string.".format(
                key
            )
            assert callable(
                sympy_
            ), "Property `sympy` of function `{}` must be a callable.".format(
                key
            )

    # Process symbol definitions
    for key in custom.get("symbols", {}).keys():

        # Ensure it's a dict
        assert isinstance(
            entry, dict
        ), "Symbol definition `{}` must be a dictionary.".format(key)

        # Update with defaults
        entry = SYMBOL_TEMPLATE.copy()
        entry.update(new_custom["symbols"][key])
        new_custom["symbols"][key] = entry

        # Basic checks
        latex_ = new_custom["symbols"][key]["latex"]
        sympy_ = new_custom["symbols"][key]["sympy"]
        assert latex_ is None or isinstance(
            latex_, str
        ), "Property `latex` of symbol `{}` must be a string.".format(key)
        assert isinstance(
            sympy_, sympy.Expr
        ), "Property `sympy` of symbol `{}` must be a SymPy expression.".format(
            key
        )

    return new_custom


def get_custom_math(user_custom_math={}):
    """
    Merge a dictionary of user-defined custom math into the default dictionary.
    Functions definitions are combined, while symbols in the user-defined
    dictionary take precedence.

    """
    # Syntax checks & make copies
    custom1 = process_custom(CUSTOM_MATH)
    custom2 = process_custom(user_custom_math)
    new_custom = custom1.copy()

    # Process function definitions
    for key, val in custom2["functions"].items():
        if key in custom1["functions"].keys():
            new_custom["functions"][key] += val
        else:
            new_custom["functions"][key] = val

    # Process symbol definitions
    for key, val in custom2["symbols"].items():
        new_custom["symbols"][key] = val

    return new_custom
