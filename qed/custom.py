import sympy

custom = {
    "functions": {
        "qEllipe": [
            {
                "description": "Complete elliptic integral of the second kind (trigonometric form)",
                "arguments": ["k^2"],
                "separators": [],
                "sympy": lambda *args: sympy.elliptic_e(
                    args[0], evaluate=False
                ),
            },
            {
                "description": "Incomplete elliptic integral of the second kind (trigonometric form)",
                "arguments": ["phi", "k^2"],
                "separators": ["|"],
                "sympy": lambda *args: sympy.elliptic_e(
                    args[0], args[1], evaluate=False
                ),
            },
            {
                "description": "Incomplete elliptic integral of the second kind (trigonometric form)",
                "arguments": ["phi", "k"],
                "separators": [","],
                "sympy": lambda *args: sympy.elliptic_e(
                    args[0], args[1] ** 2, evaluate=False
                ),
            },
            {
                "description": "Incomplete elliptic integral of the second kind (Legendre normal form)",
                "arguments": ["x", "k"],
                "separators": [";"],
                "sympy": lambda *args: sympy.elliptic_e(
                    sympy.arcsin(args[0]), args[1] ** 2, evaluate=False
                ),
            },
        ]
    },
    "symbols": {
        "qPi": {"description": "Pi", "sympy": sympy.pi},
        "qImag": {"description": "Imaginary unit", "sympy": sympy.I},
        "qEuler": {"description": "Euler's number (e)", "sympy": sympy.E},
    },
}
