import sympy

__all__ = ["CUSTOM_MATH"]


CUSTOM_MATH = {
    "functions": {
        "ellipe": [
            {
                "description": "Complete elliptic integral of the second kind (trigonometric form)",
                "arguments": ["k^2"],
                "separators": [],
                "latex": r"\mathrm{E}",
                "sympy": lambda *args: sympy.elliptic_e(
                    args[0], evaluate=False
                ),
            },
            {
                "description": "Incomplete elliptic integral of the second kind (trigonometric form)",
                "arguments": ["phi", "k^2"],
                "separators": ["|"],
                "latex": r"\mathrm{E}",
                "sympy": lambda *args: sympy.elliptic_e(
                    args[0], args[1], evaluate=False
                ),
            },
            {
                "description": "Incomplete elliptic integral of the second kind (trigonometric form)",
                "arguments": ["phi", "k"],
                "separators": [","],
                "latex": r"\mathrm{E}",
                "sympy": lambda *args: sympy.elliptic_e(
                    args[0], args[1] ** 2, evaluate=False
                ),
            },
            {
                "description": "Incomplete elliptic integral of the second kind (Legendre normal form)",
                "arguments": ["x", "k"],
                "separators": [";"],
                "latex": r"\mathrm{E}",
                "sympy": lambda *args: sympy.elliptic_e(
                    sympy.asin(args[0]), args[1] ** 2, evaluate=False
                ),
            },
        ]
    },
    "symbols": {
        "pi": {"description": "Pi", "latex": None, "sympy": sympy.pi},
        "imag": {
            "description": "Imaginary unit",
            "latex": r"i",
            "sympy": sympy.I,
        },
        "euler": {
            "description": "Euler's number (e)",
            "latex": r"e",
            "sympy": sympy.E,
        },
    },
}
